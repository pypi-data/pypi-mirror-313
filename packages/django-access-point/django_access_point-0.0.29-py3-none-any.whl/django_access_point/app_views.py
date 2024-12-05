from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from rest_framework.decorators import action

from django_access_point.models.custom_field import CUSTOM_FIELD_STATUS
from django_access_point.models.user import USER_TYPE_CHOICES, USER_STATUS_CHOICES
from django_access_point.views.custom_field import CustomFieldViewSet
from django_access_point.views.crud import CrudViewSet
from django_access_point.views.helpers_crud import (custom_field_values_related_name, _get_custom_field_queryset,
                                                     _prefetch_custom_field_values, _format_custom_field_submitted_values)
from django_access_point.utils import generate_invite_token_with_expiry, validate_invite_token
from django_access_point.utils_response import success_response, validation_error_response
from django_access_point.excel_report import ExcelReportGenerator

from .models import UserCustomField, UserCustomFieldOptions, UserCustomFieldValue
from .serializers import UserSerializer, UserCustomFieldSerializer


class PlatformUser(CrudViewSet):
    queryset = get_user_model().objects.filter(user_type=USER_TYPE_CHOICES[0][0]).exclude(
        status=USER_STATUS_CHOICES[0][0])
    list_fields = {"id": "ID", "name": "Name", "email": "Email Address", "phone_no": "phone_no"}
    list_search_fields = ["name", "email", "phone_no"]
    serializer_class = UserSerializer
    custom_field_model = UserCustomField
    custom_field_value_model = UserCustomFieldValue
    custom_field_options_model = UserCustomFieldOptions

    @action(detail=False, methods=['post'], url_path='complete-profile-setup/(?P<token_payload>.+)')
    def complete_profile_setup(self, request, token_payload, *args, **kwargs):
        """
        Complete Profile Setup with a token that includes expiry time.
        """
        # Validate the invite token
        is_valid, user, message = validate_invite_token(token_payload)

        if not is_valid:
            return validation_error_response(message)

        # Proceed with the profile setup process (e.g., update password, etc.)
        password = request.data.get('password')
        if password:
            user.set_password(password)
            user.save()

        return success_response("Profile setup completed successfully.")

    @action(detail=False, methods=['post'], url_path='generate-user-report')
    def generate_user_report(self, request, *args, **kwargs):
        """
        Generate User Report.
        """
        # Queryset to fetch active platform users
        users_queryset = self.queryset.order_by("-created_at")
        # Get User Custom Fields
        active_custom_fields = _get_custom_field_queryset(self.custom_field_model)

        # PreFetch User Custom Field Values
        users_queryset = _prefetch_custom_field_values(
            users_queryset, active_custom_fields, self.custom_field_value_model
        )

        def get_headers():
            headers = ["Name", "Email Address"]

            # Custom Field Headers
            for field in active_custom_fields:
                headers.append(field.label)

            return headers

        # Define row data for each user, including custom fields
        def get_row_data(user):
            row = [user.name, user.email]

            # Custom Field Values
            if active_custom_fields:
                if hasattr(user, custom_field_values_related_name):
                    custom_field_submitted_values = getattr(user, custom_field_values_related_name).all()
                    formatted_custom_field_submitted_values = _format_custom_field_submitted_values(
                        custom_field_submitted_values
                    )

                    # Append each custom field value to the row
                    for field in active_custom_fields:
                        row.append(formatted_custom_field_submitted_values.get(field.id, ""))

            return row

        # Create Excel report generator instance
        report_generator = ExcelReportGenerator(
            title="User Report",
            queryset=users_queryset,
            get_headers=get_headers,
            get_row_data=get_row_data
        )

        # Generate and return the report as an HTTP response
        return report_generator.generate_report()

    def after_save(self, request, instance):
        """
        Handle after save.
        """
        # After user saved, invite user to setup profile
        self.send_invite_user_email(instance)

    def send_invite_user_email(self, user):
        """
        Send the invitation email to the user with a unique token and expiry time encoded.
        """
        name = user.name
        email = user.email

        # Generate the token and encoded user ID with expiry time
        token_payload = generate_invite_token_with_expiry(user, 1)

        # Build the invite URL with the token_payload (no expiry time in the URL)
        invite_url = f"{settings.FRONTEND_URL}/profile-setup/{token_payload}/"

        # Prepare the email context
        context = {
            "user_name": name,
            "invite_url": invite_url,
            "support_email": settings.PLATFORM_SUPPORT_EMAIL,
            "platform_name": settings.PLATFORM_NAME,
            "logo_url": settings.PLATFORM_LOGO_URL,
        }

        # Render the email content (HTML)
        subject = "Invitation to Complete Your Profile"
        message = render_to_string("profile_invite_email.html", context)

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=message,  # Ensure HTML is sent
        )

        return success_response("Invitation email sent.")


class PlatformUserCustomField(CustomFieldViewSet):
    queryset = UserCustomField.objects.filter(status=CUSTOM_FIELD_STATUS[1][0]).order_by("field_order")
    serializer_class = UserCustomFieldSerializer
    custom_field_options_model = UserCustomFieldOptions

from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from django_access_point.views.helpers_crud import (
    _validate_custom_fields_attributes,
    _get_custom_field_queryset,
    _prefetch_custom_field_values,
    _get_ordering_params,
    _get_search_filter,
    _get_pagination,
    _format_custom_fields,
    _prepare_data_rows,
)
from django_access_point.utils_response import (
    success_response,
    validation_error_response,
    error_response,
    notfound_response,
    created_response,
    deleted_response,
)


class CrudViewSet(viewsets.GenericViewSet):
    """
    Base view class for CRUD operations.
    Child classes must define `queryset` and `serializer_class`.
    Optionally, `custom_field_model` and `custom_field_value_model` can also be set.
    """

    queryset = None  # Should be defined in the child class
    serializer_class = None  # Should be defined in the child class
    list_search_fields = []  # Should be defined in the child class
    custom_field_model = None  # Optional, should be defined in the child class if needed
    custom_field_value_model = None  # Optional, should be defined in the child class if needed
    custom_field_options_model = None  # Optional, should be defined in the child class if needed
    is_custom_field_enabled = False

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.custom_field_model and self.custom_field_value_model:
            self.is_custom_field_enabled = True
            context["custom_field_model"] = self.custom_field_model
            context["custom_field_value_model"] = self.custom_field_value_model
            context["custom_field_queryset"] = _get_custom_field_queryset(self.custom_field_model)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Fetch the custom field queryset from the serializer context
        custom_field_queryset = self.get_serializer_context().get("custom_field_queryset")

        # If custom field queryset exists, prefetch related custom field values
        if self.is_custom_field_enabled and custom_field_queryset:
            queryset = _prefetch_custom_field_values(
                queryset,
                custom_field_queryset,
                self.custom_field_value_model,
            )

        return queryset

    def get_list_fields(self):
        """
        This method should be overridden by child class to define the list fields,
        or the child class should define a `list_fields` attribute.
        """
        if (
            hasattr(self, "list_fields")
            and isinstance(self.list_fields, dict)
            and self.list_fields
        ):
            return self.list_fields
        else:
            raise ImproperlyConfigured(
                "Django Access Point: Either 'list_fields' or 'get_list_fields' must be defined and return a dict."
            )

    def list(self, request, *args, **kwargs):
        """
        List all objects with pagination, ordering, and search functionality.

        :param request
        :param args
        :param kwargs
        """
        _validate_custom_fields_attributes(
            self.custom_field_model, self.custom_field_value_model, self.custom_field_options_model
        )

        list_fields_to_use = self.get_list_fields()
        queryset = self.get_queryset()

        order_by = _get_ordering_params(request)
        queryset = queryset.order_by(order_by)

        search_filter = _get_search_filter(
            request,
            self.list_search_fields,
            self.custom_field_model,
            self.custom_field_value_model,
            self.is_custom_field_enabled,
        )
        queryset = queryset.filter(search_filter)

        try:
            page_obj = _get_pagination(request, queryset)
        except ValueError as e:
            return error_response(str(e))

        column_headers = list(list_fields_to_use.values())
        active_custom_fields = None

        if self.is_custom_field_enabled:
            custom_field_queryset = self.get_serializer_context().get("custom_field_queryset", None)
            if custom_field_queryset:
                active_custom_fields = _format_custom_fields(custom_field_queryset)
                column_headers += list(active_custom_fields.values())

        data = _prepare_data_rows(page_obj, list_fields_to_use, active_custom_fields, self.custom_field_options_model)

        response_data = {
            "per_page": page_obj.paginator.per_page,
            "page": page_obj.number,
            "total": page_obj.paginator.count,
            "total_pages": page_obj.paginator.num_pages,
            "columns": column_headers,
            "data": data,
        }

        return success_response(response_data)

    def create(self, request, *args, **kwargs):
        """
        Create a new object.

        :param request
        :param args
        :param kwargs
        """
        # Validate Custom Field Attributes
        _validate_custom_fields_attributes(
            self.custom_field_model, self.custom_field_value_model, self.custom_field_options_model
        )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            self.after_save(request, instance)

            return created_response(serializer.data)

        return validation_error_response(serializer.errors)

    def retrieve(self, request, pk=None, *args, **kwargs):
        """
        Retrieve a single object by primary key.

        :param request
        :param pk
        :param args
        :param kwargs
        """
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance)

        return success_response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        """
        Update an existing object by primary key.

        :param request
        :param pk
        :param args
        :param kwargs
        """
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data)

        return validation_error_response(serializer.errors)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Delete an object by primary key.

        :param request
        :param pk
        :param args
        :param kwargs
        """
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, pk=pk)
        instance.delete()

        return deleted_response("")

    def after_save(self, request, instance):
        """
        After Save

        :param request
        :param instance
        """
        pass

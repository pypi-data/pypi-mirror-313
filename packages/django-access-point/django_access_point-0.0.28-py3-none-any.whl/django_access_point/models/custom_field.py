from django.db import models

CUSTOM_FIELD_TYPE = (
    ("text_box", "Text Box"),
    ("website_url", "Website URL"),
    ("text_area", "TextArea"),
    ("number", "Number"),
    ("email", "Email"),
    ("phone_number", "Phone Number"),
    ("dropdown", "Dropdown"),
    ("radio", "Radio"), #
    ("date", "Date"), #
    ("time", "Time"), #
    ("file", "File Upload"), #
    ("multiselect_checkbox", "MultiSelect Checkbox"), #
    ("hidden", "Hidden"),
    ("heading", "Heading"), #
    ("paragraph", "Paragraph"), #
)

CUSTOM_FIELD_RULES = (
    ('required', 'Required'),
    ('minlength', 'MinLength'),
    ('maxlength', 'MaxLength'),
    ('min', 'Min'),
    ('max', 'Max'),
    ('email', 'Email'),
    ('url', 'URL'),
    ('date', 'Date'),
    ('unique', 'Unique'),
    ('number', 'Number'),
    ('max_selection', 'Max Selection'),
    ('file', 'File'),
    ('time', 'Time'),
    ('image', 'Image'),
)

CUSTOM_FIELD_RULES_DATE_FORMAT_ALLOWED = {
    'm-d-Y': '%m-%d-%Y',
    'd-m-Y': '%d-%m-%Y'
}

CUSTOM_FIELD_RULES_TIME_FORMAT_ALLOWED = {
    '12': '%I:%M %p',
    '24': '%H:%M'
}

CUSTOM_FIELD_RULES_FILE_FORMAT_ALLOWED = ["jpg", "jpeg", "png", "doc", "pdf"]

CUSTOM_FIELD_RULES_IMAGE_FORMAT_ALLOWED = ["jpg", "jpeg", "png", "gif", "bmp", "tiff", "heif", "raw", "svg"]

CUSTOM_FIELD_SIZE = (
    ("col-md-12", "Large"),
    ("col-md-6", "Medium"),
    ("col-md-4", "Small"),
)

CUSTOM_FIELD_STATUS = (
    ("deleted", "Deleted"),
    ("active", "Active"),
    ("in_active", "InActive"),
)

CUSTOM_FIELD_OPTIONS_STATUS = (
    ("deleted", "Deleted"),
    ("active", "Active"),
    ("in_active", "InActive"),
)


class CustomFieldBase(models.Model):
    label = models.TextField(max_length=200)
    slug = models.CharField(max_length=200, blank=True)
    field_type = models.CharField(max_length=20, choices=CUSTOM_FIELD_TYPE)
    field_size = models.CharField(
        max_length=20, choices=CUSTOM_FIELD_SIZE, default=CUSTOM_FIELD_SIZE[0][0]
    )
    placeholder = models.CharField(max_length=200, blank=True)
    field_order = models.PositiveIntegerField()
    custom_class_name = models.CharField(max_length=200, blank=True)
    validation_rule = models.JSONField(default=dict)
    is_unique = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    content_size = models.CharField(max_length=200, blank=True)
    content_alignment = models.CharField(max_length=200, blank=True)
    show_on_table = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20, choices=CUSTOM_FIELD_STATUS, default=CUSTOM_FIELD_STATUS[1][0]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class CustomFieldOptionsBase(models.Model):
    label = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20, choices=CUSTOM_FIELD_OPTIONS_STATUS, default=CUSTOM_FIELD_OPTIONS_STATUS[1][0]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomFieldValueBase(models.Model):
    text_field = models.TextField(blank=True)
    checkbox_field = models.BooleanField(blank=True, null=True)
    radio_field = models.CharField(max_length=255, blank=True)
    multiselect_checkbox_field = models.JSONField(null=True, default=None)
    dropdown_field = models.JSONField(null=True, default=None)
    date_field = models.DateField(blank=True,null=True,default=None)
    file_field = models.FileField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
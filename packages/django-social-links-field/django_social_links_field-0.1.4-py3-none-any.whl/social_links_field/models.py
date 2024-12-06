from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings
import json

if hasattr(settings, "SOCIAL_LINKS_FIELD_MEDIA_TYPES"):
    SOCIAL_MEDIA_TYPES = settings.SOCIAL_LINKS_FIELD_MEDIA_TYPES
else:
    SOCIAL_MEDIA_TYPES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("twitter", "Twitter"),
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("youtube", "YouTube"),
    ]


class SocialLinksWidget(forms.Widget):
    template_name = "social_links_field/social_links_widget.html"

    def format_value(self, value):
        if value and type(value) == str:
            return json.loads(value)    
        return []
    
    def get_context(self, name, value, attrs):
        ctx = {
            "name": name,
            "social_media_types": SOCIAL_MEDIA_TYPES,
            "links": self.format_value(value),
            "attrs": self.build_attrs(self.attrs, attrs or {}),
        }
        return ctx

    def value_from_datadict(self, data, files, name):
        response = []
        types = data.getlist(f"{name}_type")
        links = data.getlist(f"{name}_link")
        labels = data.getlist(f"{name}_label")
        for type_, link, label in zip(types, links, labels):
            
            if type_:
                response.append(
                    {
                        "type": type_,
                        "link": link,
                        "label": label,
                    }
                )
        return response


class SocialLinksFormField(forms.JSONField):

    def to_python(self, value):
        res = super().to_python(value) or []
        return res
    
    def __init__(self, *args, **kwargs):
        # Set default help text
        if "help_text" not in kwargs:
            kwargs["help_text"] = "Enter social media links"

        kwargs["widget"] = SocialLinksWidget
        super().__init__(*args, **kwargs)
        self.validators.append(self.json_schema_validator)

    def json_schema_validator(self, values):
        if not isinstance(values, list):
            raise ValidationError("entries must be a list.")

        for value in values:
            if "type" not in value or "link" not in value:
                raise ValidationError("Each entry must have a type and link.")

            if value["type"] not in dict(SOCIAL_MEDIA_TYPES):
                raise ValidationError("Invalid social media type.")


class SocialLinksField(models.JSONField):
    """
    A custom model field to store and validate social media links.

    Stores links in the format:
    [{
        'type': 'facebook',
        'link': 'example_user',
        'label': 'My Facebook Profile'
    }]
    """

    def __init__(self, *args, **kwargs):
        if "default" not in kwargs:
            kwargs["default"] = list
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "form_class": SocialLinksFormField,
                **kwargs,
            }
        )

    def validate(self, value, model_instance):
        super().validate(value, model_instance)

        if not isinstance(value, list):
            raise ValidationError(_("Social links must be a list of dictionaries."))

        for link in value:
            if not isinstance(link, dict):
                raise ValidationError(_("Each link must be a dictionary."))

            required_keys = ["type", "link", "label"]
            for key in required_keys:
                if key not in link:
                    raise ValidationError(_(f"Each link must have a {key}."))

            if link["type"] not in dict(SOCIAL_MEDIA_TYPES):
                raise ValidationError(_("Invalid social media type."))

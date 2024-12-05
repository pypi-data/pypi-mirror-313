from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

SOCIAL_MEDIA_TYPES = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('twitter', 'Twitter'),
    ('linkedin', 'LinkedIn'),
    ('github', 'GitHub'),
    ('youtube', 'YouTube'),
    ('custom', 'Custom'),
]

class SocialLinksWidget(forms.Widget):
    template_name = 'social_links_field/social_links_widget.html'
    
    def __init__(self, attrs=None):
        # Ensure default class for admin compatibility
        default_attrs = {'class': 'social-links-widget'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
        
    def render(self, name, value, attrs=None, renderer=None):
        # Ensure value is a list
        # Normalize value to list, handle None/empty cases
        if not value:
            value = []
        elif not isinstance(value, list):
            try:
                # Try parsing if it's a string (like from JSON field)
                import json
                value = json.loads(value)
            except (TypeError, json.JSONDecodeError):
                value = []
        
        context = {
            'name': name,
            'social_media_types': SOCIAL_MEDIA_TYPES,
            'links': value,
            'attrs': self.build_attrs(self.attrs, attrs or {})
        }
    
        
        return mark_safe(render_to_string(self.template_name, context))

    def value_from_datadict(self, data, files, name):
        # Extract links from POST data
        links = []
        types = data.getlist(f'{name}_type')
        usernames = data.getlist(f'{name}_username')
        labels = data.getlist(f'{name}_label')
        
        for type_, username, label in zip(types, usernames, labels):
            if type_ and username:
                links.append({
                    'type': type_,
                    'username': username,
                    'label': label or f'{type_.capitalize()} Link'
                })
        
        return links
    



class SocialLinksFormField(forms.JSONField):
    def __init__(self, *args, **kwargs):
        kwargs['help_text'] = 'Enter social media links'
        kwargs['widget'] = SocialLinksWidget
        super().__init__(*args, **kwargs)
    
    def validate(self, value):
        super().validate(value)
        
        if not isinstance(value, list):
            raise ValidationError('Social links must be a list.')
        
        for link in value:
            if 'type' not in link or 'username' not in link:
                raise ValidationError('Each link must have a type and username.')
            
            if link['type'] not in dict(SOCIAL_MEDIA_TYPES):
                raise ValidationError('Invalid social media type.')
            
    
    def to_python(self, value):
        # Handle various input types
        if not value:
            return []
        
        if isinstance(value, list):
            return value
        
        if isinstance(value, str):
            import json
            try:
                parsed_value = json.loads(value)
                return parsed_value if parsed_value else []
            except json.JSONDecodeError:
                raise ValidationError('Invalid JSON format')
        
        return value
    
    def prepare_value(self, value):
        # Ensure admin can display the value correctly
        if isinstance(value, list):
            import json
            return json.dumps(value)
        return value

class SocialLinksField(models.JSONField):
    """
    A custom model field to store and validate social media links.
    
    Stores links in the format:
    [{
        'type': 'facebook', 
        'username': 'example_user', 
        'label': 'My Facebook Profile'
    }]
    """
    
    def __init__(self, *args, **kwargs):
        kwargs['default'] = list
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
            raise ValidationError(_('Social links must be a list of dictionaries.'))
        
        for link in value:
            if not isinstance(link, dict):
                raise ValidationError(_('Each link must be a dictionary.'))
            
            required_keys = ['type', 'username', 'label']
            for key in required_keys:
                if key not in link:
                    raise ValidationError(_(f'Each link must have a {key}.'))
            
            if link['type'] not in dict(SOCIAL_MEDIA_TYPES):
                raise ValidationError(_('Invalid social media type.'))
    
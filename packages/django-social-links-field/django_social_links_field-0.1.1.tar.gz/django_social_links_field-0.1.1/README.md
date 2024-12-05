# Django Social Links Field

## Overview

`social-links-field` is a Django package that provides a custom model field, form field, and widget for managing social media links with ease. It allows developers to store and manage multiple social media links for a model with built-in validation and a user-friendly interface.


![Admin Panel Screenshot](./social_links_field/screenshot.png?raw=true)

## Features

- Custom JSON-based field for storing social media links
- Predefined social media platforms
- Dynamic form widget for adding/removing social links
- Built-in validation
- Easy integration with Django forms and admin interface



## Installation

Install the package using pip:

```bash
pip install django-social-links-field
```


## Quick Start

### 1. Add to INSTALLED_APPS

In your Django project's `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'social_links_field',
    ...
]
```

### 2. Use in Models

```python
from django.db import models
from social_links_field.models import SocialLinksField

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    social_links = SocialLinksField()
```

### 3. In Django Admin

The field automatically works with Django admin:

```python
from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # No special configuration needed
    pass
```

## Supported Social Media Platforms

- Facebook
- Instagram
- Twitter
- LinkedIn
- GitHub
- YouTube
- Custom

Configure the downdown values from `settings.py`
```
SOCIAL_LINKS_FIELD_MEDIA_TYPES = [
    # value, label
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "Twitter"),
    ("linkedin", "LinkedIn"),
    ("github", "GitHub"),
    ("youtube", "YouTube"),
]

```

## Data Structure

Social links are stored as a list of dictionaries:

```python
[
    {
        'type': 'facebook', 
        'username': 'example_user', 
        'label': 'My Facebook Profile'
    }
]
```

## Form Usage

```python
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'social_links']
```

## Customization

### Adding Custom Social Media Platforms

You can extend `SOCIAL_MEDIA_TYPES` in your project:

```python
from social_links_field.models import SOCIAL_MEDIA_TYPES

SOCIAL_MEDIA_TYPES += [
    ('tiktok', 'TikTok'),
    ('telegram', 'Telegram')
]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License
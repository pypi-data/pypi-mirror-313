from django.db import models
from social_links_field.models import SocialLinksField

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    social_links = SocialLinksField(blank=True)

    def __str__(self):
        return self.name
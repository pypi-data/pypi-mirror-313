from django.contrib import admin
from .models import UserProfile
from django.forms import ModelForm

class UserProfileAdmin(admin.ModelAdmin):
    def save_form(self, request, form, change):
        # Print the data before saving
        # {'name': 'Check Empty', 'social_links': None}
        print(form.clean())
        res = super().save_form(request, form, change)
        print("cleaned_data", form.cleaned_data, res.social_links)
        return res

admin.site.register(UserProfile, UserProfileAdmin)

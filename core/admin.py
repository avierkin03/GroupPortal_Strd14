from django.contrib import admin

# Register your models here.
from .models import GroupProfile, UserProfile

admin.site.register(GroupProfile)
admin.site.register(UserProfile)

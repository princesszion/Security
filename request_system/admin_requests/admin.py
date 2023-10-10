from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role')  # Add 'role' here

admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'company_name', 'email')}),
        ('Права', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    list_display = ('username', 'company_name', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ['username', 'email', 'company_name']


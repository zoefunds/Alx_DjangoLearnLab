from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin interface for CustomUser model.
    """
    
    # Fields to display in the list view
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'is_email_verified',
        'created_at'
    )
    
    # Fields to search in the admin interface
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    
    # Fields to filter in the admin interface
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'is_email_verified',
        'created_at',
        'updated_at'
    )
    
    # Ordering in the list view
    ordering = ('-created_at',)
    
    # Define fieldsets for the change form
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Information'), {
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'phone_number',
                'profile_photo',
                'bio'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        (_('Email Verification'), {
            'fields': ('is_email_verified',)
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Define fieldsets for the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
        (_('Personal Information'), {
            'classes': ('wide',),
            'fields': (
                'first_name',
                'last_name',
                'date_of_birth',
                'phone_number',
                'profile_photo',
                'bio'
            )
        }),
        (_('Permissions'), {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )
    
    # Make these fields read-only
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    
    # Filter horizontal for many-to-many fields
    filter_horizontal = ('groups', 'user_permissions')


# Register the CustomUser model with the admin
admin.site.register(CustomUser, CustomUserAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser


class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin configuration for the CustomUser model.
    """
    
    # Fields to display in the list view
    list_display = (
        'email',
        'username',
        'first_name',
        'last_name',
        'date_of_birth',
        'is_staff',
        'is_active',
        'profile_photo_preview',
        'created_at'
    )
    
    # Fields to filter by
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'created_at',
        'date_of_birth',
    )
    
    # Fields to search by
    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
    )
    
    # Ordering
    ordering = ('-created_at',)
    
    # Define fieldsets for add and change forms
    fieldsets = (
        ('Account Information', {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Fieldsets for the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo'),
        }),
        ('Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    
    def profile_photo_preview(self, obj):
        """Display profile photo as a thumbnail in the list view."""
        if obj.profile_photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_photo.url
            )
        return 'No photo'
    
    profile_photo_preview.short_description = 'Photo'


# Register the custom user model with the admin
admin.site.register(CustomUser, CustomUserAdmin)
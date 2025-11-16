from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for handling user creation with additional fields.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Custom user model extending AbstractUser with additional fields.
    """
    
    # Override username to make it optional since we're using email as primary identifier
    username = models.CharField(max_length=150, blank=True, null=True)
    
    # Custom fields
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Date of Birth'),
        help_text=_('User\'s date of birth (optional)')
    )
    profile_photo = models.ImageField(
        upload_to='profile_photos/%Y/%m/%d/',
        null=True,
        blank=True,
        verbose_name=_('Profile Photo'),
        help_text=_('User\'s profile photo (optional)')
    )
    
    # Additional useful fields
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_('Phone Number')
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name=_('Biography')
    )
    is_email_verified = models.BooleanField(
        default=False,
        verbose_name=_('Email Verified')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    # Set the custom manager
    objects = CustomUserManager()
    
    # Use email as the unique identifier for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Return the user's full name.
        """
        return f"{self.first_name} {self.last_name}".strip()
    
    def get_short_name(self):
        """
        Return the user's short name.
        """
        return self.first_name
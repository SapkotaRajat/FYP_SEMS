# user_authentication/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import mark_safe

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)  

class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True)
    username = models.CharField(max_length=150, unique=True)  # Ensure uniqueness
    address = CKEditor5Field(null=True)
    USERNAME_FIELD = 'username'
        
    # Unique related names to resolve clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='user'
    )
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = CKEditor5Field(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='static/profile_pictures/', null=True, blank=True)
    attended_events = models.ManyToManyField('event_management.Event', blank=True)
    ticket_purchases = models.ManyToManyField('ticket_purchase.Ticket', blank=True) 
    

    def __str__(self):
        return self.user.username   
    
    def image_tag(self):
        if self.profile_picture:
            return mark_safe('<img src="{url}" width="{width}" height="{height}" style="object-fit: cover;"/>'.format(
                url=self.profile_picture.url,
                width=100,
                height=100,
            ))
            
        else:
            return None
# user_authentication/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile
from django.utils.html import mark_safe

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    model = CustomUser
    list_display = ['username','email', 'first_name', 'last_name', 'is_active', 'is_staff', 'display_profile_picture']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'contact_number', 'dob')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'contact_number', 'dob', 'is_active', 'is_staff', 'groups', 'user_permissions'),
        }),
    )
    
    def display_profile_picture(self, obj):
        if obj.userprofile.profile_picture:
            return mark_safe('<img src="{url}" width="{width}" height="{height}" style="object-fit: cover;" />'.format(
                url=obj.userprofile.profile_picture.url,
                width=100,
                height=100,
            ))
        else:
            return None

    display_profile_picture.short_description = 'Profile Picture'

admin.site.register(CustomUser, CustomUserAdmin)

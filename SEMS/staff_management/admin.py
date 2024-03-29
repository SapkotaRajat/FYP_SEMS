from django.contrib import admin
from django.contrib import messages
from .models import StaffApplication
from user_authentication.models import CustomUser as User

@admin.register(StaffApplication)
class StaffApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position_desired', 'created_at')
    search_fields = ('first_name', 'last_name', 'position_desired')
    list_filter = ('position_desired', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('position_desired', 'first_name', 'last_name', 'address', 'street_address', 'address_line_2', 'city', 'state_province_region', 'zip_postal_code', 'country', 'email', 'phone', 'referred_by', 'convicted', 'convicted_explanation', 'school_name', 'highest_grade_completed', 'graduate', 'consent', 'resume', 'class_schedule', 'approved')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.approved:
            try:
                # Get the user object
                user = User.objects.get(email=obj.email)
                # Update is_staff field
                user.is_staff = True
                user.save()
                print('User is now staff.')
                messages.success(request, f"The user '{user.email}' has been marked as staff.")
            except User.DoesNotExist:
                messages.error(request, f"No user found with email '{obj.email}'.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

        super().save_model(request, obj, form, change)


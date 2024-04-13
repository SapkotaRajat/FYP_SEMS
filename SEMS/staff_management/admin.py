from django.contrib import admin
from django.contrib import messages
from .models import StaffApplication
from user_authentication.models import CustomUser as User
from django.core.mail import send_mail
from django.utils.html import strip_tags 

@admin.register(StaffApplication)
class StaffApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position_desired', 'created_at', 'approval_status')
    search_fields = ('first_name', 'last_name', 'position_desired')
    list_filter = ('position_desired', 'created_at', 'approval_status')
    fieldsets = (
        (None, {
            'fields': ('position_desired', 'first_name', 'last_name', 'address', 'street_address', 
                       'address_line_2', 'city', 'state_province_region', 'zip_postal_code', 'country', 
                       'email', 'phone', 'referred_by', 'convicted', 'convicted_explanation', 'school_name', 
                       'highest_grade_completed', 'graduate', 'consent', 'resume', 'class_schedule', 'approval_status', 'rejection_message')
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Save the object first

        # Check if 'approved' has changed to 'yes' or 'no'
        if 'approval_status' in form.changed_data:
            if obj.approval_status == 'yes':
                # Update user to staff if not already
                user = User.objects.get(email=obj.email)
                if not user.is_staff:
                    user.is_staff = True
                    user.save()
                    messages.success(request, f"The user '{user.email}' has been marked as staff.")
                
                # Send an approval email
                send_mail(
                    'Staff Application Approved',
                    'Congratulations! Your application has been approved. You are now a staff member.',
                    'sapkotarajat59@gmial.com',  # Replace with your sender email
                    [user.email],
                    fail_silently=False,
                )
            elif obj.approval_status == 'no':
                user = User.objects.get(email=obj.email)
                # Send a rejection email
                clean_message = strip_tags(obj.rejection_message)  # Apply strip_tags here
                message_body = f'We regret to inform you that your application has been rejected.\n{clean_message}'
                send_mail(
                    'Staff Application Rejected',
                    message_body,
                    'sapkotarajat59@gmail.com',  # Ensure correct spelling of 'gmail'
                    [obj.email],
                    fail_silently=False,
                )
                if user.is_staff:
                    user = User.objects.get(email=obj.email)
                    user.is_staff = False
                    user.save()
                    
        messages.success(request, f"The user '{user.email}' has been removed from staff.")
        if obj.approval_status == 'yes' and not change:  # If new and approved
            messages.info(request, "Approval email sent to the user.")
        elif obj.approval_status == 'no' and not change:  # If new and rejected
            messages.info(request, "Rejection email sent to the user.")


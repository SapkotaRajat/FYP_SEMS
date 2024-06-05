from django.contrib import admin
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.core.serializers.json import DjangoJSONEncoder
from ticket_purchase.models import TicketPurchase, Ticket
from event_management.models import Event, Category, Organizer, EventVacancy
from user_authentication.models import CustomUser, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from staff_management.models import StaffApplication
from core.models import Policy, Position, PositionsCategory, BannerImage
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html
import json
import calendar
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.html import strip_tags
from user_authentication.models import CustomUser as User


class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        # Calculate total ticket purchases
        total_tickets_sold = TicketPurchase.objects.count()
        
        # Calculate total events
        total_events = Event.objects.count()
        
        # Calculate total users
        total_users = CustomUser.objects.count()
        
        # Calculate total contacts (assuming UserProfile represents contacts)
        total_contacts = UserProfile.objects.count()
        
        # Calculate total earnings
        total_earnings = TicketPurchase.objects.aggregate(total_earnings=Sum('payment_amount'))['total_earnings']
        total_earnings = Decimal(total_earnings) if total_earnings is not None else Decimal(0)
        
        # Calculate monthly earnings
        monthly_earnings = TicketPurchase.objects.annotate(
            month=ExtractMonth('date')
        ).values('month').annotate(
            total_earnings=Sum('payment_amount')
        ).order_by('month')
        
        # Create a dictionary to map month numbers to month names
        month_names = {i: calendar.month_name[i] for i in range(1, 13)}

        # Convert monthly earnings data to a list of dictionaries with month names as labels
        monthly_earnings_data = [
            {
                'month': month_names[entry['month']],
                'total_earnings': float(entry['total_earnings'])
            } for entry in monthly_earnings
        ]
        
        # Convert monthly earnings data to JSON string
        monthly_earnings_json = json.dumps(monthly_earnings_data, cls=DjangoJSONEncoder)
        
        # Query admin log entries
        admin_logs = LogEntry.objects.all()[:10]  # Adjust the number of entries as needed
        
        # Calculate event data
        event_data = []
        events = Event.objects.all()
        for event in events:
            total_expenses = Decimal(0)  # Initialize as Decimal
            # count the number of assigned_staff for each event
            staff_assignments = EventVacancy.objects.filter(event=event, assigned_staff__isnull=False).values_list('assigned_staff', flat=True)
            for assignment in staff_assignments:
                vacancies = EventVacancy.objects.filter(event=event, assigned_staff=assignment)
                for vacancy in vacancies:
                    start_datetime = datetime.combine(vacancy.date, vacancy.start_time)
                    end_datetime = datetime.combine(vacancy.date, vacancy.end_time)
                    duration_hours = Decimal((end_datetime - start_datetime).total_seconds() / 3600)
                    payment_hourly = Decimal(vacancy.payment_hourly)  # Ensure payment_hourly is Decimal
                    expense = duration_hours * payment_hourly
                    rounded_expense = expense.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                    total_expenses += rounded_expense
            event_expenses = Decimal(event.expenses) if event.expenses else Decimal(0)
            total_event_earnings = TicketPurchase.objects.filter(event=event).aggregate(total_earnings=Sum('payment_amount'))['total_earnings'] or Decimal(0)
            total_event_earnings = Decimal(total_event_earnings)

            data = {
                'event_title': event.title,
                'total_tickets_sold': TicketPurchase.objects.filter(event=event).count(),
                'total_staff_assigned': staff_assignments.count(),
                'total_expenses': total_expenses + event_expenses,
                'total_earnings': total_event_earnings,
                'profit': total_event_earnings - (total_expenses + event_expenses)
            }
            event_data.append(data)
            
        # Update extra_context with calculated totals and event data
        extra_context = extra_context or {}
        extra_context.update({
            'total_tickets_sold': total_tickets_sold,
            'total_events': total_events,
            'total_users': total_users,
            'total_contacts': total_contacts,
            'total_amount_paid': float(total_earnings),
            'monthly_earnings': monthly_earnings_json,
            'admin_logs': admin_logs,
            'event_data': event_data,
        })

        return super().index(request, extra_context)

# Register the custom admin site
custom_admin_site = CustomAdminSite()

# Register models with the custom admin site
# ticket purchase

class TicketAdmin(admin.ModelAdmin):   
    model = Ticket
    list_display = ['event', 'price', 'available_quantity', 'ticket_date']
    search_fields = ['event', 'price', 'available_quantity', 'ticket_date']
    ordering = ['event']
    
    fieldsets = (
        (None, {'fields': ('event', 'price', 'available_quantity', 'ticket_date')}),
        ('Ticket Description', {'fields': ('ticket_description',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('event', 'ticket_price', 'available_quantity', 'ticket_date', 'ticket_description'),
        }),
    )

class TicketPurchaseAdmin(admin.ModelAdmin):
    model = TicketPurchase
    list_display = ['user','image_tag',  'date','order_id', 'quantity',  'payment_method', 'payment_amount', 'event', 'email', 'payer_name', 'payee_country', 'ticket_qr','ticket']
    search_fields = ['order_id', 'user', 'date', 'ticket', 'quantity', 'payment_method', 'payment_amount', 'event', 'email', 'payer_name', 'payee_country']
    ordering = ['-date']
    
    fieldsets = (
        (None, {'fields': ('order_id', 'user', 'ticket', 'quantity', 'payment_method', 'payment_amount', 'event', 'email', 'payer_name', 'payee_country', 'ticket_qr')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('order_id', 'user', 'ticket', 'quantity', 'payment_method', 'payment_amount', 'event', 'email', 'payer_name', 'payee_country', 'ticket_qr'),
        }),
    )
    
    def image_tag(self, obj):
        print(obj.ticket_qr.url)
        if obj.ticket_qr:
            return format_html('<img src="{}" width="100" height="100" />'.format(
                obj.ticket_qr.url),
                width=100,
                height=100,
                )
        else:
            return None
    image_tag.short_description = 'Ticket QR'
    
custom_admin_site.register(TicketPurchase, TicketPurchaseAdmin)


class EventVacancyInline(admin.TabularInline):
    model = EventVacancy
    extra = 4
    

class EventAdmin(admin.ModelAdmin):
    list_display = ('title',  'image_tag', 'date', 'start_time','end_time', 'location', 'category', 'organizer')
    # add search bar to search for events
    search_fields = ['title', 'date', 'location']
    inlines = [EventVacancyInline]  

custom_admin_site.register(Ticket, TicketAdmin)
custom_admin_site.register(Event,EventAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','image_tag',)
    
custom_admin_site.register(Category, CategoryAdmin)
custom_admin_site.register(Organizer)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

class EventVacancyProfileInline(admin.TabularInline):
    model = EventVacancy
    fields = ['event', 'position', 'date', 'start_time', 'end_time', 'payment_hourly', 'assigned_staff', 'total_earnings']
    readonly_fields = ['event', 'position', 'date', 'start_time', 'end_time', 'payment_hourly', 'assigned_staff', 'total_earnings']
    extra = 0
    verbose_name_plural = 'Event Vacancies'
    
    def total_earnings(self, instance):
        if instance.date:  # Check if instance.date is not None
            start_datetime = datetime.combine(instance.date, instance.start_time)
            end_datetime = datetime.combine(instance.date, instance.end_time)
            duration_hours = (end_datetime - start_datetime).total_seconds() / 3600
            total_earnings = round(Decimal(duration_hours) * instance.payment_hourly, 2)
            return total_earnings
        else:
            return None
    
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)
        if 'total_earnings' not in fields:
            fields += ['total_earnings']
        return fields

class CustomUserAdmin(UserAdmin):
    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj:
            inlines.append(UserProfileInline(self.model, self.admin_site))
            if obj.is_staff and not obj.is_superuser:
                inlines.append(EventVacancyProfileInline(self.model, self.admin_site))
        return inlines
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

custom_admin_site.register(CustomUser, CustomUserAdmin)
custom_admin_site.register(Policy)
custom_admin_site.register(Position)
custom_admin_site.register(PositionsCategory)
custom_admin_site.register(Group)


class BannerImageAdmin(admin.ModelAdmin):
    list_display = ['image_url', 'image_tag']
    
    def image_tag(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height="{height}" style="object-fit: cover;" />'.format(
            url=obj.image_url.url,
            width=100,
            height=100,
        ))
    image_tag.short_description = 'Image'

custom_admin_site.register(BannerImage, BannerImageAdmin)



class StaffApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position_desired', 'created_at', 'approval_status')
    search_fields = ('first_name', 'last_name', 'position_desired')
    list_filter = ('position_desired', 'created_at', 'approval_status')
    fieldsets = (
        (None, {
            'fields': ('position_desired', 'first_name', 'last_name', 'address', 'street_address', 
                       'address_line_2', 'city', 'state_province_region', 'zip_postal_code', 'country', 
                       'email', 'phone', 'referred_by', 'convicted', 'convicted_explanation', 'school_name', 
                       'highest_grade_completed', 'graduate', 'consent', 'resume', 'class_schedule', 
                       'approval_status', 'rejection_message')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Check if 'approval_status' has changed
        if 'approval_status' in form.changed_data:
            print(f"Approval status changed to: {obj.approval_status}")  # Debugging: Log approval status change
            try:
                user = User.objects.get(email=obj.email)
                if obj.approval_status == 'yes':
                    if not user.is_staff:
                        user.is_staff = True
                        user.save()
                        messages.success(request, f"The user '{user.email}' has been marked as staff.")
                    send_mail(
                        'Staff Application Approved',
                        'Congratulations! Your application has been approved. You are now a staff member.',
                        'sapkotarajat59@gmail.com', 
                        [user.email],
                        fail_silently=False,
                    )
                elif obj.approval_status == 'no':
                    clean_message = strip_tags(obj.rejection_message)
                    message_body = f'We regret to inform you that your application has been rejected.\n{clean_message}'
                    send_mail(
                        'Staff Application Rejected',
                        message_body,
                        'sapkotarajat59@gmail.com',  # Ensure correct spelling of 'gmail'
                        [obj.email],
                        fail_silently=False,
                    )
                    if user.is_staff:
                        user.is_staff = False
                        user.save()
                        messages.success(request, f"The user '{user.email}' has been removed from staff.")
            except User.DoesNotExist:
                messages.error(request, f"No user found with email '{obj.email}'")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
            print(f"User status updated based on approval status: {obj.approval_status}")  # Debugging: Confirmation of status update

        if obj.approval_status == 'yes':
            messages.info(request, "Approval email sent to the user.")
        elif obj.approval_status == 'no':
            messages.info(request, "Rejection email sent to the user.")
        super().save_model(request, obj, form, change)
        
custom_admin_site.register(StaffApplication, StaffApplicationAdmin)

# Assign the custom admin site to admin.site
admin.site = custom_admin_site

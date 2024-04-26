from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from django.core.serializers.json import DjangoJSONEncoder
import json
import calendar
from ticket_purchase.models import TicketPurchase, Ticket
from event_management.models import Event, Category, Organizer, StaffAssignment, EventVacancy
from user_authentication.models import CustomUser, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from staff_management.models import StaffApplication
from core.models import Policy, Position, PositionsCategory
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry
from django.utils.html import format_html

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
        total_earnings = total_earnings if total_earnings is not None else 0
        
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
        
        # Update extra_context with calculated totals
        extra_context = extra_context or {}
        extra_context.update({
            'total_tickets_sold': total_tickets_sold,
            'total_events': total_events,
            'total_users': total_users,
            'total_contacts': total_contacts,
            'total_amount_paid': total_earnings,
            'monthly_earnings': monthly_earnings_json,
            'admin_logs': admin_logs,
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



####

class EventVacancyInline(admin.TabularInline):
    model = EventVacancy
    extra = 4
    

class EventAdmin(admin.ModelAdmin):
    list_display = ('title',  'image_tag', 'date', 'start_time','end_time', 'location', 'category', 'organizer')
    inlines = [EventVacancyInline]  

custom_admin_site.register(Ticket, TicketAdmin)
custom_admin_site.register(Event,EventAdmin)
custom_admin_site.register(Category)
custom_admin_site.register(Organizer)
custom_admin_site.register(StaffAssignment)

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

custom_admin_site.register(CustomUser, CustomUserAdmin)
custom_admin_site.register(StaffApplication)
custom_admin_site.register(Policy)
custom_admin_site.register(Position)
custom_admin_site.register(PositionsCategory)
custom_admin_site.register(Group)
# Assign the custom admin site to admin.site
admin.site = custom_admin_site

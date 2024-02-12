from django.contrib import admin
from .models import Category, Event, Ticket, Attendee, StaffAssignment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time', 'location', 'category', 'organizer')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'is_paid')

@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')

@admin.register(StaffAssignment)
class StaffAssignmentAdmin(admin.ModelAdmin):
    list_display = ('get_staff_names', 'event', 'role', 'assigned_by', 'assigned_at')

    def get_staff_names(self, obj):
        return ', '.join([staff.username for staff in obj.staff.all()])
    get_staff_names.short_description = 'Staff'

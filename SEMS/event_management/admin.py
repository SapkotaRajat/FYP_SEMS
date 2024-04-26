from django.contrib import admin
from .models import Category, Event, StaffAssignment, Organizer, EventVacancy

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','image_tag',)

@admin.register(StaffAssignment)
class StaffAssignmentAdmin(admin.ModelAdmin):
    list_display = ('get_staff_names', 'event', 'role', 'assigned_by', 'assigned_at')

    def get_staff_names(self, obj):
        return ', '.join([staff.username for staff in obj.staff.all()])
    get_staff_names.short_description = 'Staff'
    
@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization','image_tag',)
    
    def user(self, obj):
        return obj.user.username
    

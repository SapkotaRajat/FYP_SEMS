from django.contrib import admin
from .models import StaffApplication, Positions, PositionsCategory
from django.utils.html import mark_safe


@admin.register(StaffApplication)
class StaffApplicationAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'position_desired', 'email', 'created_at']
    list_filter = ['position_desired', 'graduate', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'street_address', 'address_line_2',
                       'city', 'state_province_region', 'zip_postal_code', 'country')
        }),
        ('Application Details', {
            'fields': ('position_desired', 'referred_by', 'convicted', 'convicted_explanation' ,'school_name', 'highest_grade_completed', 'graduate', 'consent')
        }),
        ('Attachments', {
            'fields': ('resume', 'class_schedule')
        }),
        ('Admin Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
@admin.register(PositionsCategory)
class PositionsCategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
    search_fields = ['category']
    fieldsets = (
        ('Category Information', {
            'fields': ('category', 'category_description')
        }),
    )
    
@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ['position', 'category']
    search_fields = ['position', 'category']
    fieldsets = (
        ('Position Information', {
            'fields': ('position', 'category', 'position_description')
        }),
    )
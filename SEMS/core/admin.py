from django.contrib import admin
from .models import Position, PositionsCategory, Policy
from django.utils.html import mark_safe
   
@admin.register(PositionsCategory)
class PositionsCategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
    search_fields = ['category']
    fieldsets = (
        ('Category Information', {
            'fields': ('category', 'category_description')
        }),
    )
    
@admin.register(Position)
class PositionsAdmin(admin.ModelAdmin):
    list_display = ['position', 'category']
    search_fields = ['position', 'category']
    fieldsets = (
        ('Position Information', {
            'fields': ('position', 'category', 'position_description')
        }),
    )

    
@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Policy Information', {
            'fields': ('title', 'content', 'created_at')
        }),
    )
    def content(self, obj):
        return mark_safe(obj.content)
    content.short_description = 'Content'

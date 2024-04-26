from django.contrib import admin
from .models import Ticket, TicketPurchase, Income
from django.utils.html import format_html
# Register your models here.


class IncomeAdmin(admin.ModelAdmin):
    model = Income
    list_display = ['event', 'date', 'amount']
    search_fields = ['event', 'date', 'amount']
    ordering = ['-date']
    
    fieldsets = (
        (None, {'fields': ('event', 'date', 'amount')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('event', 'date', 'amount'),
        }),
    )
    
admin.site.register(Income, IncomeAdmin)


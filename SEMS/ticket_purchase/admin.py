from django.contrib import admin
from .models import Ticket
# Register your models here.


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
    
    
admin.site.register(Ticket, TicketAdmin)


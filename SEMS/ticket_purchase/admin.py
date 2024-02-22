from django.contrib import admin
from .models import Ticket, TicketPurchase
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


class TicketPurchaseAdmin(admin.ModelAdmin):
    model = TicketPurchase
    list_display = ['order_id', 'user', 'date', 'ticket', 'quantity', 'payment_method', 'payment_amount', 'event', 'email', 'payer_name', 'payee_country']
    search_fields = ['order_id', 'user', 'date', 'ticket', 'quantity', 'payment_method', 'payment_amount', 'event', 'email', 'payer_name', 'payee_country']
    ordering = ['-date']
    
    fieldsets = (
        (None, {'fields': ('order_id', 'user', 'ticket', 'quantity', 'payment_method', 'payment_amount', 'event', 'email', 'payer_name', 'payee_country')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('order_id', 'user', 'ticket', 'quantity', 'payment_method', 'payment_amount', 'event', 'email', 'payer_name', 'payee_country'),
        }),
    )
    
admin.site.register(TicketPurchase, TicketPurchaseAdmin)
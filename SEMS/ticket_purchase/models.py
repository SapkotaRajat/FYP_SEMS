from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from event_management.models import Event
from django.conf import settings

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity  = models.IntegerField()
    ticket_description = CKEditor5Field()
    ticket_date = models.DateField()
    
    def __str__(self):
        return self.event.title
    


class TicketPurchase(models.Model):
    order_id = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField()
    payer_name = models.CharField(max_length=100)
    payee_country = models.CharField(max_length=100)
    ticket_qr = models.FileField(upload_to='static/tickets/', null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.user.username} - {self.ticket.event.title} - {self.date}"
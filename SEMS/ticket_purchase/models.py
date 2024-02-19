from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from event_management.models import Event

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity  = models.IntegerField()
    ticket_description = CKEditor5Field()
    ticket_date = models.DateField()
    
    def __str__(self):
        return self.event.title
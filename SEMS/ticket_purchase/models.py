from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.
class Ticket(models.Model):
    event_name = models.CharField(max_length=100)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_quantity_available = models.IntegerField()
    ticket_type = models.CharField(max_length=100)
    ticket_description = CKEditor5Field
    ticket_image = models.ImageField(upload_to='images/')
    ticket_date = models.DateField()
    ticket_time = models.TimeField()
    
    
    def __str__(self):
        return self.event_name
    
class Payment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    ticket_quantity = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16 , null=True, blank=True)
    card_expiry_date = models.DateField( null=True, blank=True)
    card_cvv = models.CharField(max_length=3 , null=True, blank=True)
    bank_name = models.CharField(max_length=100 , null=True, blank=True)
    account_name = models.CharField(max_length=100 , null=True, blank=True)
    account_number = models.CharField(max_length=100 , null=True, blank=True)
    payment_method = models.CharField(max_length=100)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_screenshot = models.ImageField(upload_to='images/')
    is_confirmed = models.BooleanField(default=False)
    confirmed_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='confirmed_by', on_delete=models.CASCADE, null=True, blank=True)
    confirmed_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.ticket.event_name} - {self.user.username}"

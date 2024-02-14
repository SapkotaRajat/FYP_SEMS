# ticket_purchase/forms.py

# forms.py

from django import forms
from event_management.models import Event

PAYMENT_METHOD_CHOICES = [
    ('', 'Select Payment Method'),
    ('card', 'Credit/Debit Card'),
    ('qr', 'QR Code'),]

class BuyTicketsForm(forms.Form):
    ticket_quantity = forms.IntegerField(label='Ticket Quantity' , min_value=1, max_value=10, required=True )
    payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_METHOD_CHOICES , required=True)
    payment_amount = forms.DecimalField(label='Payment Amount', required=False)
    card_holder_name = forms.CharField(label='Card Holder Name', required=False)
    card_number = forms.CharField(label='Card Number', required=False)
    expiry_month = forms.CharField(label='Expiry Month', required=False)
    expiry_year = forms.CharField(label='Expiry Year', required=False)
    cvv = forms.CharField(label='CVV', required=False)
    qr_code_image = forms.ImageField(label='QR Code Image', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize the payment method choices if needed
        self.fields['payment_method'].choices = PAYMENT_METHOD_CHOICES



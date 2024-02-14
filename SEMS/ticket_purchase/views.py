from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BuyTicketsForm
from .models import Ticket, Payment

# Create your views here.
def ticket_purchase(request):
    return render(request, 'tickets.html' )

@login_required
def buy_tickets(request, event_name):
    if request.method == 'POST':
        ticket_purchase_form = BuyTicketsForm(request.POST, request.FILES)
        if ticket_purchase_form.is_valid():
            # Extract form data
            ticket_quantity = ticket_purchase_form.cleaned_data['ticket_quantity']
            payment_method = ticket_purchase_form.cleaned_data['payment_method']
            payment_amount = ticket_purchase_form.cleaned_data['payment_amount']
            card_holder_name = ticket_purchase_form.cleaned_data['card_holder_name']
            card_number = ticket_purchase_form.cleaned_data['card_number']
            expiry_month = ticket_purchase_form.cleaned_data['expiry_month']
            expiry_year = ticket_purchase_form.cleaned_data['expiry_year']
            cvv = ticket_purchase_form.cleaned_data['cvv']
            qr_code_image = ticket_purchase_form.cleaned_data['qr_code_image']
            
            # Save ticket details
            ticket = Ticket.objects.get(event_name=event_name)
            
            # Save payment details
            payment = Payment.objects.create(
                ticket=ticket,
                payment_method=payment_method,
                payment_amount=payment_amount,
                card_holder_name=card_holder_name,
                card_number=card_number,
                expiry_month=expiry_month,
                expiry_year=expiry_year,
                cvv=cvv,
                qr_code_image=qr_code_image,
                # Add other payment details here
            )
            
            # Redirect to the ticket purchase success page
            return redirect('ticket-purchase-success')
    else:
        ticket_purchase_form = BuyTicketsForm()
    
    return render(request, 'buy-tickets.html', {'ticket_purchase_form': ticket_purchase_form, 'event_name': event_name})
@login_required
def ticket_purchase_success(request):
    return render(request, 'ticket-purchase-success.html')

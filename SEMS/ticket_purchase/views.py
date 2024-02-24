import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket 
from event_management.models import Event
from .models import TicketPurchase

# Create your views here.
def ticket_purchase(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets.html' , {'tickets': tickets})

@login_required
def buy_tickets(request, event_name):
    event = Event.objects.get(title=event_name)
    user_has_purchased_tickets = TicketPurchase.objects.filter(event=event, user=request.user).exists()
    ticket_purchases = TicketPurchase.objects.filter(event=event, user=request.user)
    # total count of the tickets purchased by the user for the event can be multiple entries in the database 
    ticket_purchased = 0 
    for ticket_purchase in ticket_purchases:
        ticket_purchased += ticket_purchase.quantity
    
    return render(request, 'buy-tickets.html', { 'event': event, 'user_has_purchased_tickets': user_has_purchased_tickets, 'ticket_purchased': ticket_purchased})


@login_required
def ticket_purchase_success(request):
    return render(request, 'ticket-purchase-success.html')


def paypal_transaction_complete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('orderID')
        payment_amount = data.get('paymentAmount')
        payment_method = 'PayPal'
        quantity = data.get('quantity')
        ticket = Ticket.objects.get(event = data.get('event'))
        event = ticket.event
        email = data.get('payeeEmail')
        payer_name = data.get('payerName') + ' ' + data.get('payerSurname')
        payee_country = data.get('payeeCountry')
               
        # Save the transaction details to the database
        ticket_purchase = TicketPurchase(order_id=order_id, user=request.user, ticket=ticket, quantity=quantity, payment_method=payment_method, payment_amount=payment_amount, event=event, email=email, payer_name=payer_name, payee_country=payee_country)
        ticket_purchase.save()
        
        # reduce the available quantity from the ticket table in the database 
        ticket.available_quantity -= int(quantity)
        ticket.save()
        
        return JsonResponse({'message': 'Transaction completed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
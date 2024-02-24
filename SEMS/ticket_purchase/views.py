import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket 
from event_management.models import Event
from django.http import JsonResponse
from .models import TicketPurchase
import json
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.core.files import File
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import render_to_string

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


@login_required
def paypal_transaction_complete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('orderID')
        payment_amount = data.get('paymentAmount')
        payment_method = 'PayPal'
        quantity = data.get('quantity')
        ticket = Ticket.objects.get(event=data.get('event'))
        event = ticket.event
        email = data.get('payeeEmail')
        payer_name = data.get('payerName') + ' ' + data.get('payerSurname')
        payee_country = data.get('payeeCountry')

        # Save the transaction details to the database
        ticket_purchase = TicketPurchase(order_id=order_id, user=request.user, ticket=ticket, quantity=quantity,
                                         payment_method=payment_method, payment_amount=payment_amount, event=event,
                                         email=email, payer_name=payer_name, payee_country=payee_country)
        ticket_purchase.save()

        # reduce the available quantity from the ticket table in the database
        ticket.available_quantity -= int(quantity)
        ticket.save()

        # Generate QR Code for the ticket
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'Purchase ID: {order_id}')
        qr.make(fit=True)

        # Save QR code image as a file
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = f'qr_{payer_name}_{event}_{ticket}.png'  # Adjusted the file name format
        img.save(img_path)
        # Add a short delay to ensure the file is fully saved
        # Associate the QR code image path with the ticket_purchase model
        ticket_purchase.ticket_qr.save(f'qr_{payer_name}_{event}_{ticket}.png', File(open(img_path, 'rb')))
        # Render ticket details and QR code into HTML
        html_content = render_to_string('email/purchase_successful.html', {
            'payer_name': payer_name,
            'event_title': event.title,
            'quantity': quantity,
            'payment_amount': payment_amount,
            'qr_code_image': img_path,
        })
        # Convert HTML to PDF
        pdf_file = BytesIO()
        pisa.CreatePDF(BytesIO(html_content.encode('utf-8')), dest=pdf_file)

        # Reset the file pointer to the beginning
        pdf_file.seek(0)

        # Send an email to the user
        subject = 'Thank You for Your Purchase!'
        message = render_to_string('email/purchase_successful.html', {
            'user': request.user,
            'event_title': event.title,
            'payment_amount': payment_amount,
            'quantity': quantity,
        })
        email = EmailMessage(subject, message, to=[request.user.email])
        email.content_subtype = 'html'
        
        # Attach PDF to the email
        email.attach(f'purchase_{order_id}.pdf', pdf_file.getvalue(), 'application/pdf')

        # Send the email
        email.send()
        os.remove(img_path)

        return JsonResponse({'message': 'Transaction completed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})


    
def purchase_successful(request):
    return render(request, 'email/purchase_successful.html')


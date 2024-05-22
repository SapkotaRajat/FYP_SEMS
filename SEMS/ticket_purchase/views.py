import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Ticket, TicketPurchase
from event_management.models import Event
from django.http import JsonResponse
import json
from django.core.mail import EmailMessage
import qrcode
from reportlab.lib.pagesizes import letter
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.core.files import File
from django.utils import timezone
from django.conf import settings

# Create your views here.
def ticket_purchase(request):
    # tickets of the upcoming events only
    tickets = Ticket.objects.filter(event__date__gte=timezone.now())
    return render(request, 'tickets.html' , {'tickets': tickets})

@login_required
def buy_tickets(request, event_name):
    event = Event.objects.get(title=event_name)
    user_has_purchased_tickets = TicketPurchase.objects.filter(event=event, user=request.user).exists()
    ticket_purchases = TicketPurchase.objects.filter(event=event, user=request.user)
    ticket_available = Ticket.objects.get(event=event).available_quantity
    # total count of the tickets purchased by the user for the event can be multiple entries in the database 
    ticket_purchased = 0 
    for ticket_purchase in ticket_purchases:
        ticket_purchased += ticket_purchase.quantity
    
    return render(request, 'buy-tickets.html', { 'event': event, 'user_has_purchased_tickets': user_has_purchased_tickets, 'ticket_purchased': ticket_purchased, 'ticket_available': int(ticket_available)})


@login_required
def ticket_purchase_success(request):
    return render(request, 'ticket-purchase-success.html')

@login_required
def paypal_transaction_complete(request):
    if request.method == 'POST':
        user = request.user
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
        ticket_purchase = TicketPurchase(
            order_id=order_id, user=request.user, ticket=ticket, quantity=quantity,
            payment_method=payment_method, payment_amount=payment_amount, event=event,
            email=email, payer_name=payer_name, payee_country=payee_country
        )
        ticket_purchase.save()

        # Reduce the available quantity from the ticket table in the database
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
        img = qr.make_image(fill_color="black", back_color="white")

        # Sanitize the file name
        sanitized_name = sanitize_filename(f'qr_{payer_name}_{event}_{ticket}.png')
        img_path = os.path.join(settings.MEDIA_ROOT, 'qr_codes', sanitized_name)
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        img.save(img_path)

        # Save the QR code image path to the database
        with open(img_path, 'rb') as f:
            ticket_purchase.ticket_qr.save(sanitized_name, File(f))
        ticket_purchase.save()

        # Generate PDF for the ticket
        pdf_content = generate_pdf(order_id, user.first_name, event.title, quantity, payment_amount, event.date, event.start_time, img_path)

        # Send an email to the user
        subject = 'Thank You for Your Purchase with Sajilo Events!'
        message = (
            f'Dear {user.first_name},\n\nThank you for choosing Sajilo Events for your ticket purchase. Your support means a lot to us.\n\n'
            f'We are pleased to confirm your successful purchase for the following event:\n\n'
            f'Event: {event.title}\n'
            f'Date: {event.date}\n'
            f'Quantity: {quantity}\n'
            f'Total Amount: {payment_amount}\n\n'
            'Payment Details:\n'
            f'Payment Method: {payment_method}\n'
            f'Order ID: {order_id}\n\n'
            'For your convenience, we have attached a PDF copy of your ticket to this email. Please present the ticket at the event venue for entry.\n\n'
            'Should you have any questions or need further assistance, feel free to reach out to us at sajiloevents@gmail.com. Our team is here to help.\n\n'
            'Thank you once again for your purchase. We look forward to welcoming you to the event and ensuring you have a memorable experience.\n\n'
            'Best regards,\n'
            'Sajilo Events Team\n'
            'sajiloevents@gmail.com'
        )
        email = EmailMessage(subject, message, to=[request.user.email])
        email.content_subtype = 'plain'
        email.attach(f'purchase_{order_id}.pdf', pdf_content, 'application/pdf')
        email.send()

        # Clean up: remove the generated QR code file
        os.remove(img_path)

        return JsonResponse({'message': 'Transaction completed successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

def sanitize_filename(filename):
    """
    Sanitize the filename by removing invalid characters and limiting its length.
    """
    import re
    filename = re.sub(r'[^a-zA-Z0-9_-]', '_', filename)
    return filename[:50]  # Shorten the filename if it's too long

def generate_pdf(order_id, payer_name, event_title, quantity, payment_amount, event_date, event_time, qr_code_image):
    buffer = BytesIO()

    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    style_body = styles['BodyText']
    style_body.alignment = 0

    # Add content to the PDF
    content = []

    content.append(Paragraph(f'Dear {payer_name},', style_body))
    content.append(Spacer(1, 12))
    content.append(Paragraph('Thank you for your purchase with Sajilo Events!', style_body))
    content.append(Spacer(1, 12))
    content.append(Paragraph('Please find your ticket details below:', style_body))
    content.append(Spacer(1, 12))
    content.append(Paragraph(f'Event: {event_title}', style_body))
    content.append(Paragraph(f'Date: {event_date}', style_body))
    content.append(Paragraph(f'Time: {event_time}', style_body))
    content.append(Paragraph(f'Quantity: {quantity}', style_body))
    content.append(Paragraph(f'Total Payment Amount: ${payment_amount}', style_body))
    content.append(Paragraph(f'Order ID: {order_id}', style_body))
    content.append(Spacer(1, 12))
    content.append(Paragraph('Please present this ticket at the event venue for entry.', style_body))
    content.append(Spacer(1, 12))
    content.append(Paragraph('Thank you for choosing Sajilo Events. We look forward to welcoming you to the event!', style_body))
    content.append(Spacer(1, 12))
    content.append(Image(qr_code_image, width=200, height=200))

    # Build PDF
    pdf.build(content)

    buffer.seek(0)
    return buffer.getvalue()

def purchase_successful(request):
    context = {
        'order_id': '1234567890',
        'payer_name': 'John Doe',
        'event_title': 'Music Concert',
        'quantity': 2,
        'date': '2022-12-31',
        'time': '18:00',
        'payment_amount': 50.00,
        'qr_code_image': ' /static/tickets/qr_Ellen_Sapkota_Photography_Masterclass_Photography_Masterclass_3U9FsT5.png',
    }   

    return render(request, 'email/purchase_successful.html' , context)


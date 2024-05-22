# app/user_authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from .models import CustomUser
from .forms import ProfilePictureForm
from .models import UserProfile
from ticket_purchase.models import TicketPurchase
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
import qrcode
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from django.http import HttpResponse
from datetime import date, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER


def redirect_if_logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # If user is logged in, redirect to home page or any other desired page
            return redirect('home')  # Change 'home' to the name of your home page URL
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

@redirect_if_logged_in
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name').strip()
        last_name = request.POST.get('last_name').strip()
        email = request.POST.get('email').strip()
        username = request.POST.get('username').strip()
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')

        errors = {}

        # Check if the first name is empty or only whitespace
        if not first_name:
            errors['first_name_error'] = 'First name cannot be empty or whitespace only.'

        # Check if the last name is empty or only whitespace
        if not last_name:
            errors['last_name_error'] = 'Last name cannot be empty or whitespace only.'

        # Check if the username is empty or only whitespace
        if not username:
            errors['username_error'] = 'Username cannot be empty or whitespace only.'
        elif CustomUser.objects.filter(username=username).exists():
            errors['username_error'] = 'Username is already taken.'

        # Check if the email is already registered
        if CustomUser.objects.filter(email=email).exists():
            errors['email_error'] = 'Email is already registered.'

        # Validate password requirements
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password):
            errors['password_error'] = 'Password must be at least 8 characters long and contain at least one uppercase letter and one digit.'

        # Check if the passwords match
        if password != password2:
            errors['confirm_password_error'] = 'Passwords do not match.'

        # If there are any errors, re-render the form with errors
        if errors:
            return render(request, 'register.html', {
                **errors,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'username': username,
                'password1': password,
                'password2': password2
            })

        # If all checks pass, create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        return render(request, 'login.html', {
            'username': username,
            'password': password,
            'registered': 'true'
        })

    return render(request, 'register.html')


@redirect_if_logged_in
def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            next_page = request.GET.get('next')
            print(next_page)
            if next_page:
                return redirect(next_page)
            return redirect('profile')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.' , 'username': username, 'password': password})

    return render(request, 'login.html')

@login_required
def logout_request(request):
    logout(request)
    return redirect('login')

@login_required
def logout_confirmation(request):
    return render(request, 'logout.html')
@login_required
def profile(request):
    return render(request, 'profile/profile.html', {})
@login_required
def change_password(request):
    # Implement your password reset logic here
    return render(request, 'change-password.html', {})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password-reset.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'
    form_class = PasswordResetForm

    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # Add your custom validation logic here
        email = form.cleaned_data['email']
        print(email)
        
        # Check if the email exists in the database
        if CustomUser.objects.filter(email=email).exists():
            # User is registered, proceed with the default behavior
            return super().form_valid(form)
        else:
            # User is not registered, add an error message
            messages.error(self.request, 'No accounts found with that email address.')
            # Render the form again with the error message
            return self.render_to_response(self.get_context_data(form=form))
@login_required
def change_profile_picture(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
    
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)  # Return success status code
    else:
        form = ProfilePictureForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def account_settings(request):
    min_age = date.today() - timedelta(days=365*16)
    return render(request, 'profile/account-settings.html', { 'min_age': min_age.strftime("%Y-%m-%d")})

@login_required
def update_profile(request):
    if request.method == 'POST':
        # Extract form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        
        # Get the logged-in user
        user = request.user
        
        # If email exists raise the error 
        if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            return render(request, 'profile/account-settings.html', {'email_error': 'Email is already registered.' , 'first_name': first_name, 'last_name': last_name, 'email': email, 'contact_number': contact_number, 'address': address, 'dob': dob})
        # Update user data
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.contact_number = contact_number
        user.address = address
        
        
        # Ensure dob is converted to date object
        if dob:
            user.dob = date.fromisoformat(dob)
        
        data = [first_name,last_name,email,contact_number,address,dob]
        print(data)
        # Save user object
        user.save()
        
        return redirect('profile')  # Redirect to profile page after saving
    
@login_required
def ticket_history(request):
    # Get all ticket purchases for the current user
    ticket_purchases = TicketPurchase.objects.filter(user=request.user)

    # Handle filtering options
    sort_by = request.GET.get('sort_by')
    if sort_by == 'date':
        ticket_purchases = ticket_purchases.order_by('event__date')
    elif sort_by == 'event_title':
        ticket_purchases = ticket_purchases.order_by('event__title')
    elif sort_by == 'total_cost':
        ticket_purchases = ticket_purchases.annotate(total_cost=Sum('payment_amount')).order_by('total_cost')

    # Group ticket purchases by event ID
    grouped_ticket_purchases = {}
    for ticket_purchase in ticket_purchases:
        event_id = ticket_purchase.event.id
        if event_id not in grouped_ticket_purchases:
            grouped_ticket_purchases[event_id] = [ticket_purchase]
        else:
            grouped_ticket_purchases[event_id].append(ticket_purchase)

    return render(request, 'profile/ticket-history.html', {'grouped_ticket_purchases': grouped_ticket_purchases})

@login_required
def attended_events(request):
    # pass the events of which the user has purchased tickets and the event has already passed 
    ticket_purchase = TicketPurchase.objects.filter(user=request.user, event__date__lt=date.today())
    return render(request, 'profile/attended-events.html', {'ticket_purchase': ticket_purchase})

@login_required
def download_ticket(request, ticket_id):
    ticket_purchase = TicketPurchase.objects.get(id=ticket_id)
    user = ticket_purchase.user

    # Generate QR Code for the ticket
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'Ticket ID: {ticket_id}')
    qr.make(fit=True)

    img_path = f'qr_{ticket_id}.png'
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(img_path)

    # Create a PDF document
    ticket_pdf_path = f'ticket_{user.username}_{ticket_purchase.event.title}.pdf'
    doc = SimpleDocTemplate(ticket_pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    style_heading = styles["Heading1"]
    style_heading.alignment = TA_CENTER
    style_body = ParagraphStyle(name='BodyText', parent=styles['Normal'], alignment=TA_CENTER)

    # Define content for the PDF
    content = []

    # Title
    content.append(Paragraph("Your Event Ticket", style_heading))
    content.append(Spacer(1, 0.5 * inch))

    # Event Details
    event_details = [
        ["Event:", ticket_purchase.event.title],
        ["Location:", ticket_purchase.event.location],
        ["Date:", ticket_purchase.event.date.strftime('%B %d, %Y')],
        ["Time:", f"{ticket_purchase.event.start_time.strftime('%I:%M %p')} - {ticket_purchase.event.end_time.strftime('%I:%M %p')}"],
    ]
    event_table = Table(event_details, colWidths=[2*inch, 4*inch])
    content.append(event_table)
    content.append(Spacer(1, 0.5 * inch))

    # Ticket Details
    ticket_details = [
        ["Quantity:", ticket_purchase.quantity],
        ["Total:", f"${ticket_purchase.payment_amount}"],
    ]
    ticket_table = Table(ticket_details, colWidths=[2*inch, 4*inch])
    content.append(ticket_table)
    content.append(Spacer(1, 0.5 * inch))

    # User Information
    user_details = [
        ["Name:", f"{user.first_name} {user.last_name}"],
        ["Email:", user.email],
        ["Contact Number:", user.contact_number],
        ["Date of Birth:", user.dob.strftime('%B %d, %Y')],
    ]
    user_table = Table(user_details, colWidths=[2*inch, 4*inch])
    content.append(user_table)
    content.append(Spacer(1, 0.5 * inch))

    # QR Code
    qr_image = Image(img_path, width=1.5*inch, height=1.5*inch)
    content.append(Paragraph("Scan QR Code for Ticket Details", style_body))
    content.append(Spacer(1, 0.2 * inch))
    content.append(qr_image)

    # Build the PDF document
    doc.build(content)

    # Return the PDF file as a response
    return FileResponse(open(ticket_pdf_path, 'rb'), as_attachment=True)


def get_ticket_details(request, ticket_id):
    ticket = get_object_or_404(TicketPurchase, id=ticket_id)
    # Assuming you have a serializer to serialize ticket data into JSON
    # Format the start and end time objects as strings
    start_time_str = ticket.event.start_time.strftime("%I:%M %p")
    end_time_str = ticket.event.end_time.strftime("%I:%M %p")
    
    # Construct the time range string
    time_range_str = f"{start_time_str} - {end_time_str}"
    ticket_data = {
        'event': {
            'title': ticket.event.title,
            'date': ticket.event.date,
            'time': time_range_str,
            'location': ticket.event.location,
            'ticket_price': ticket.event.ticket_price,
        },
        'quantity': ticket.quantity,
        'payment_amount': ticket.payment_amount,
    }
    return JsonResponse(ticket_data)

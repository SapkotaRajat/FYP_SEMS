# app/user_authentication/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm , LoginForm
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
from reportlab.pdfgen import canvas
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import date, timedelta



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user to the database
            form.save()
            messages.success(request, 'Registration successful')            
            # Redirect to the home page or another page after successful registration
            return redirect('login')
        else:
            # Display specific error messages for each field
            for field, errors in form.errors.items():
                print(field, errors)
                for error in errors:
                    # Set error messages for each form field
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Authentication failed')
        else:
            # Check for non-field errors and display the first one
            non_field_errors = form.errors.get('__all__')
            if non_field_errors:
                print(non_field_errors)
                
            else:
                for field, errors in form.errors.items():
                    errors.append(errors[0])
                    print(field, errors)
            messages.error(request, form.errors['__all__'])

    else:
        form = LoginForm()

    return render(request, 'login.html', {'login_form': form})

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
    print(grouped_ticket_purchases)

    return render(request, 'profile/ticket-history.html', {'grouped_ticket_purchases': grouped_ticket_purchases})



@login_required
def attended_events(request):
    return render(request, 'profile/attended-events.html', {})

@login_required
def assigned_tasks(request):
    return render(request, 'profile/assigned-tasks.html', {})

@login_required
def work_history(request):
    return render(request, 'profile/work-history.html', {})

@login_required
def download_ticket(request, ticket_id):
    ticket = TicketPurchase.objects.get(id=ticket_id)
    
    # Generate QR Code for the ticket
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f'Ticket ID: {ticket_id}')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Render ticket details and QR code into a PDF
    ticket_pdf_path = f'ticket_{ticket_id}.pdf'
    with open(ticket_pdf_path, 'wb') as pdf_file:
        pdf = canvas.Canvas(pdf_file, pagesize=letter)

        pdf.drawString(100, 750, f"Event: {ticket.event.title}")
        
        # Add other ticket details to the PDF
        
        img_path = f'qr_{ticket_id}.png'
        img.save(img_path)
        pdf.drawInlineImage(img_path, 100, 550, width=100, height=100)  # Draw QR code

        pdf.showPage()
        pdf.save()

    # Return a response with the PDF file
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

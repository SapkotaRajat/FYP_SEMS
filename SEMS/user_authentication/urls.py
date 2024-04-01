#user_authentication/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomPasswordResetView

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_confirmation, name='logout_confirmation'),
    path('logout/confirm/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password-reset-done.html'
        ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password-reset-confirm.html'
        ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password-reset-complete.html'
        ), name='password_reset_complete'),
    path('change-password/', views.change_password, name='change_password'),
    path('change_profile_picture/', views.change_profile_picture, name='change_profile_picture'),
    path('account-settings/', views.account_settings, name='account_settings'),
    path('ticket-history/', views.ticket_history, name='ticket_history'),
    path('attended-events/', views.attended_events, name='attended_events'),
    path('download-ticket/<int:ticket_id>', views.download_ticket, name='download-ticket'),
    path('api/tickets/<int:ticket_id>/', views.get_ticket_details, name='get_ticket_details'),
    path('update-profile/', views.update_profile, name='update_profile'),
    
    
]
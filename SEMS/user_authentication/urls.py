from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_confirmation, name='logout_confirmation'),
    path('logout/confirm/', views.logout_request, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('profile/', views.profile, name='profile'),
    
]
from django.contrib import admin
from django.contrib import messages
from .models import StaffApplication
from django.core.mail import send_mail
from django.utils.html import strip_tags

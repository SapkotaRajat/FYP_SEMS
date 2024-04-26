"""
URL configuration for sems project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.conf.urls import handler404


urlpatterns = [
    path('', core_views.index, name='home'),
    path('admin/', admin.site.urls),
    path('', include('user_authentication.urls')),
    path('', include('staff_management.urls')),
    path('', include('ticket_purchase.urls')),
    path('', include('core.urls')),
    path('', include('event_management.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    
]

handler404 = 'core.views.custom_404'
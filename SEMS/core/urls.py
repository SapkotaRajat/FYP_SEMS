from django.urls import path
from . import views
from django.conf.urls import handler404
handler404 = 'accounts.views.custom_404'

urlpatterns = [
    path("404",views.error,name='error'),
    path("error",views.custom_404,name='error'),
    re_path(r'^.*/$', views.custom_404),
]
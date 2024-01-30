from django.urls import path
from . import views
from django.conf.urls import handler404
handler404 = 'core.views.custom_404'

urlpatterns = [
    path("404",views.error,name='error'),
    path("error",views.custom_404,name='error'),
    path('',views.index,name='index'),
    path('plan-your-visit/',views.plan_your_visit,name='plan-your-visit'),
    path('about-us/',views.about,name='about-us'),
]
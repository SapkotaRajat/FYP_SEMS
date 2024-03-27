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
    path('policies/',views.policies,name='policies'),
    path('specifications/',views.specifications,name='specifications'),
    path('employment/',views.employment,name='employment'),
    path('venue-booking/',views.venue_booking,name='venue-booking'),
    path('contact-us/',views.contact_us,name='contact-us'),
    path('faq/',views.faq,name='faq'),
    path('terms-and-conditions/',views.terms_and_conditions,name='terms-and-conditions'),
    path('privacy-policy/',views.privacy_policy,name='privacy-policy'),
    path('refund-policy/',views.refund_policy,name='refund-policy'),
    path('staff-application/',views.staff_application,name='staff-application'),
    path('staff-application/success/',views.success,name='success-page'),
]
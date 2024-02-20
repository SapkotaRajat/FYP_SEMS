from django.urls import path
from . import views

urlpatterns = [
    path('tickets/', views.ticket_purchase, name='tickets'),
    path('buy-tickets/<str:event_name>', views.buy_tickets, name='buy-tickets'),
    path('ticket-purchase-success/', views.ticket_purchase_success, name='ticket-purchase-success'),
    path('paypal-transaction-complete/', views.paypal_transaction_complete, name='paypal_transaction_complete'),
]

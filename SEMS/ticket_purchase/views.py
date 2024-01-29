from django.shortcuts import render

# Create your views here.
def ticket_purchase(request):
    return render(request, 'ticket_purchase.html', {})
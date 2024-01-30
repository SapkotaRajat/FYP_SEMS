from django.shortcuts import render

# Create your views here.
def ticket_purchase(request):
    context = {}
    return render(request, 'ticket_purchase.html' , context)
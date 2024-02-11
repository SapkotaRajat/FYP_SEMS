from django.shortcuts import render

# Create your views here.

def events_and_tickets(request):
    return render(request, 'events-and-tickets.html')

def events_categories(request):
    return render(request, 'events-categories.html')

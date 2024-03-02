from django import template
from event_management.models import Event
from django.utils import timezone

register = template.Library()

@register.simple_tag

def upcoming_events():
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:4]
    return upcoming_events


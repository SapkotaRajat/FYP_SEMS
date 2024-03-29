import json
from django.core.management.base import BaseCommand
from event_management.models import Event
from ticket_purchase.models import Ticket
import os

class Command(BaseCommand):
    help = 'Create tickets for events based on JSON fixture data'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('event_management', 'fixtures', 'events.json')
        with open(file_path, 'r') as file:
            events_data = json.load(file)

        for event_data in events_data:
            event_title = event_data['title']
            try:
                event = Event.objects.get(title=event_title)
                ticket_price = event_data['ticket_price']
                ticket_quantity = event_data.get('ticket_quantity', 0)  # You may need to adjust this depending on your JSON structure
                ticket_description = event_data.get('ticket_description', '')

                ticket = Ticket.objects.create(
                    event=event,
                    price=ticket_price,
                    available_quantity=ticket_quantity,
                    ticket_description=ticket_description,
                    ticket_date=event.date
                )

                self.stdout.write(self.style.SUCCESS(f"Created ticket for event: {event_title}"))
            except Event.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"Event '{event_title}' not found. Skipping ticket creation."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error creating ticket for event '{event_title}': {str(e)}"))

import json
import os
from django.core.management.base import BaseCommand
from event_management.models import Event  # Import your Event model


class Command(BaseCommand):
    help = 'Load events data into the database'

    def handle(self, *args, **options):
        file_path = os.path.join('event_management', 'fixtures', 'events.json')
        with open(file_path, 'r') as file:
            events_data = json.load(file)
            for event_data in events_data:
                Event.objects.create(**event_data)
        self.stdout.write(self.style.SUCCESS('Events data loaded successfully'))

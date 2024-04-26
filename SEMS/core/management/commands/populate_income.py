from django.core.management.base import BaseCommand
from ticket_purchase.models import TicketPurchase, Income
from event_management.models import Event

class Command(BaseCommand):
    help = 'Populates the Income model with data from previous ticket purchases'

    def handle(self, *args, **kwargs):
        # Clear existing Income objects if needed
        Income.objects.all().delete()

        # Retrieve ticket purchase data
        ticket_purchases = TicketPurchase.objects.all()

        # Calculate total income per event
        income_per_event = {}
        for purchase in ticket_purchases:
            event_title = purchase.event.title
            amount = purchase.payment_amount
            if event_title in income_per_event:
                income_per_event[event_title] += amount
            else:
                income_per_event[event_title] = amount

        # Create Income objects and save them
        for event_title, total_income in income_per_event.items():
            event = Event.objects.get(title=event_title)
            income = Income.objects.create(event=event, amount=total_income)
            self.stdout.write(self.style.SUCCESS(f"Income record created for {event_title}"))

        self.stdout.write(self.style.SUCCESS('Income data population completed'))
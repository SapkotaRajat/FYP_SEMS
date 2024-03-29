import os
import json
from django.core.management.base import BaseCommand
from core.models import Policy

class Command(BaseCommand):
    help = 'Load policy data from a JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('core', 'fixtures', 'policies.json')
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                policies_data = json.load(file)
                for policy_data in policies_data:
                    title = policy_data.get('fields', {}).get('title')
                    content = policy_data.get('fields', {}).get('content')
                    if title and content:
                        Policy.objects.create(title=title, content=content)
                        self.stdout.write(self.style.SUCCESS('Policy "{}" loaded successfully!'.format(title)))
                    else:
                        self.stdout.write(self.style.WARNING('Skipping policy creation. Title or content missing.'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('File not found. Please provide the correct file path.'))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Error decoding JSON. Please check the file format.'))


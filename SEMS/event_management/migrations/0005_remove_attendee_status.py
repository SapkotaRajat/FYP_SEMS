# Generated by Django 5.0.1 on 2024-02-27 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0004_attendee_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendee',
            name='status',
        ),
    ]

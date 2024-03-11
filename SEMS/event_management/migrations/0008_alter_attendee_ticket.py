# Generated by Django 5.0.1 on 2024-02-27 18:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0007_attendee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ticket', to='event_management.ticketdetail'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-04-06 15:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0012_alter_staffassignment_role'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='staffassignment',
            name='staff1',
            field=models.ManyToManyField(related_name='staff1', to=settings.AUTH_USER_MODEL),
        ),
    ]

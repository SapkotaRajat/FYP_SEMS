from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/category_images/')
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='static/event_images/')
    description = CKEditor5Field()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ticket_available = models.BooleanField(default=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    dress_code = models.CharField(max_length=100, blank=True, null=True)
    special_guests = models.TextField(blank=True, null=True)
    parking_info = models.CharField(max_length=200, blank=True, null=True)
    transportation_options = models.TextField(blank=True, null=True)
    accessibility_info = models.TextField(blank=True, null=True)
    food_and_beverage = models.TextField(blank=True, null=True)
    rules_and_regulations = models.TextField(blank=True, null=True)
    sponsors = models.TextField(blank=True, null=True)
    contact_info = models.CharField(max_length=200, blank=True, null=True)
    social_media_links = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Attendee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

class StaffAssignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL)
    role = models.CharField(max_length=100)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_by', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{', '.join([staff.username for staff in self.staff.all()])} - {self.event.title}"

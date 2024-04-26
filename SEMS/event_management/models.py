from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import mark_safe
from core.models import Position
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/category_images/')
    def __str__(self):
        return self.name
    
    def image_tag(self):
        if self.image: 
            return mark_safe('<img src="{url}" width="{width}" height="{height}" style="object-fit: cover;" />'.format(
                url=self.image.url,
                width=100,
                height=100,
            ))
        else:
            return None 
    image_tag.short_description = 'Image'
    
class Organizer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200)
    organization_image = models.ImageField(upload_to='static/organizer_images/')
    organization_description = CKEditor5Field()
    organization_website = models.URLField(blank=True, null=True)
    organization_email = models.EmailField(blank=True, null=True)
    organization_phone = models.CharField(max_length=15, blank=True, null=True)    
    
    def __str__(self):
        return self.organization
    
    def image_tag(self):
        if self.organization_image:
            return mark_safe('<img src="{url}" width="{width}" height="{height}" style="object-fit: cover;" />'.format(
                url=self.organization_image.url,
                width=100,
                height=100,
            ))
        else:
            return None
    image_tag.short_description = 'Image'

class Event(models.Model):
    title = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to='static/event_images/')
    description = CKEditor5Field()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE, null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ticket_available = models.BooleanField(default=True)
    capacity = models.CharField(max_length=100, blank=True, null=True)
    special_guests = CKEditor5Field(blank=True, null=True)
    parking_info = models.CharField(max_length=200, blank=True, null=True)
    transportation_options = CKEditor5Field(blank=True, null=True)
    food_and_beverage = CKEditor5Field(blank=True, null=True)
    rules_and_regulations = CKEditor5Field(blank=True, null=True)
    sponsors = CKEditor5Field(blank=True, null=True)

    def __str__(self):
        return self.title
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="{url}" width="{width}" height="{height}" style="object-fit: cover;" />'.format(
                url=self.image.url,
                width=100,
                height=100,
            ))
        else:
            return None
    image_tag.short_description = 'Image'


class StaffAssignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL)
    role = models.ForeignKey(Position, on_delete=models.CASCADE)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_by')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{', '.join([staff.username for staff in self.staff.all()])} - {self.event.title}"

class EventVacancy(models.Model):
    class DateSourceChoices(models.TextChoices):
        EVENT_DATE = 'event', _('Use Event Date')
        CUSTOM_DATE = 'custom', _('Use Custom Date')

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_source = models.CharField(
        max_length=10,
        choices=DateSourceChoices.choices,
        default=DateSourceChoices.EVENT_DATE
    )
    date = models.DateField(null=True, blank=True)  # Custom date, can be null if using event date
    start_time = models.TimeField()
    end_time = models.TimeField()
    payment_hourly = models.DecimalField(max_digits=10, decimal_places=2,default=20.00)
    assigned_staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.date_source == self.DateSourceChoices.EVENT_DATE:
            # Set date from the event
            self.date = self.event.date
        # No else needed; if CUSTOM_DATE is chosen, the date should be whatever is manually set in self.date
        super(EventVacancy, self).save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.position} - {self.event.title}"

from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.html import mark_safe

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
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

class TicketDetail(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(TicketDetail, on_delete=models.CASCADE, related_name='ticket', null=True, blank=True)

class StaffAssignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL)
    role = models.CharField(max_length=100)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assigned_by', on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{', '.join([staff.username for staff in self.staff.all()])} - {self.event.title}"

# staff_management/models.py
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class StaffApplication(models.Model):
    position_desired = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_province_region = models.CharField(max_length=100)
    zip_postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    referred_by = models.CharField(max_length=100, blank=True, null=True)
    convicted = models.BooleanField()
    convicted_explanation = CKEditor5Field(blank=True, null=True)
    school_name = models.CharField(max_length=100)
    highest_grade_completed = models.CharField(max_length=20)
    graduate = models.BooleanField()
    consent = models.BooleanField()
    resume = models.FileField(upload_to='resumes/')
    class_schedule = models.FileField(upload_to='class_schedules/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position_desired}"


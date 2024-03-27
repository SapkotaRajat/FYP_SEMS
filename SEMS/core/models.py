from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class StaffApplication(models.Model):
    position_desired = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
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
    class_schedule = models.FileField(upload_to='class_schedules/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position_desired}"

class PositionsCategory(models.Model):
    category = models.CharField(max_length=100)
    category_description = CKEditor5Field()

    def __str__(self):
        return self.category    
    
class Positions(models.Model):
    category = models.ForeignKey(PositionsCategory, related_name='positions',on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    position_description = CKEditor5Field()
    

    def __str__(self):
        return self.position

class Policy(models.Model):
    title = models.CharField(max_length=100)
    content = CKEditor5Field()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
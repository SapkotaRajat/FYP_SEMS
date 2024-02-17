# staff_management/models.py
from django.db import models
from user_authentication.models import CustomUser

class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    work_experience = models.CharField(max_length=100, blank=True, null=True)
    qualifications = models.CharField(max_length=255, blank=True, null=True)
    

    def __str__(self):
        return self.user.username

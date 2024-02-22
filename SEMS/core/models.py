from django.db import models

# Create your models here.

class BannerImage(models.Model):
    full_image = models.ImageField(upload_to='images/')
    wide_image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
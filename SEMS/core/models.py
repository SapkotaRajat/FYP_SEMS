from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class PositionsCategory(models.Model):
    category = models.CharField(max_length=100)
    category_description = CKEditor5Field()

    def __str__(self):
        return self.category    
    
class Position(models.Model):
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
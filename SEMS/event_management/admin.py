from django.contrib import admin
from .models import Organizer, EventVacancy



@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization','image_tag',)
    
    def user(self, obj):
        return obj.user.username
    

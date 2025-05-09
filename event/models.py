from django.db import models
from django.urls import reverse


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='events/')
    
    def event_day(self):
        return self.date.strftime('%d')
    
    def event_month(self):
        return self.date.strftime('%b').upper()
    
    def time_range(self):
        return f"{self.start_time.strftime('%I:%M%p')}-{self.end_time.strftime('%I:%M%p')}"
    
    def get_absolute_url(self):
        return reverse("event_detail", args=[str(self.pk)])

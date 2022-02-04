from datetime import datetime,date
from django.db import models
from django.urls import reverse
from accounts.models import User
from django.db import models
class EventAbstract(models.Model):

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class EventManager(models.Manager):
    def get_all_events(self, user):
        events = Event.objects.filter(
            user=user, is_active=True, is_deleted=False
        )
        return events

    def get_running_events(self, user):
        # return events with gte to get end times less than or equal to the date (this filters current events)
        running_events = Event.objects.filter(
            user=user, is_active=True, is_deleted=False,
            end_time__gte=datetime.now().date()
        ).order_by('start_time')
        return running_events


class Event(EventAbstract):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events'
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    outfrnt_task = models.BooleanField(default=False)
    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('calendarapp:event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('calendarapp:event-detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
        
    @property
    def is_due(self):
        return datetime.now() > self.end_time
    
class Archived(EventAbstract):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    objects = EventManager()
    
    def __str__ (self):
        return self.title 
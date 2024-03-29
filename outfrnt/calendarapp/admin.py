from django.contrib import admin
from calendarapp import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = [
        'id', 'title', 'user', 'is_active','outfrnt_task', 'is_deleted', 'created_at',
        'updated_at'
    ]
    list_filter = ['is_active', 'is_deleted']
    search_fields = ['title']


@admin.register(models.Archived)

class ArchivedAdmin(admin.ModelAdmin):
    model = models.Archived
    list_display = [
        'id', 'title', 'user' , 'description',
    ]
    search_fields = ['title']
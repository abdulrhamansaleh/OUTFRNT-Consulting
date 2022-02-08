from django.urls import path
from . import views

app_name = 'calendarapp'

urlpatterns = [
    path('client/calendar-task-view/', views.CalendarViewNew.as_view(), name='calendar'),
    path('all-event-list/', views.all_events_view, name = "all_events"),
    path('running-event-list/', views.current_events_view, name = "running_events"),
    path('add/task-outfrnt', views.outfrnt_tasks, name = "outfrnt_task"),
    path('delete-task/<str:event_id>', views.delete_task, name = "delete_task"),
    path('delete-task-outfrnt/<str:event_id>', views.delete_outfrnt_task, name = "delete"),
    path('view-details-task/<str:event_id>', views.detail_task_view , name = "task-details")
]

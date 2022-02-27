from django.urls import path
from . import views

app_name = 'calendarapp'

urlpatterns = [
    path('client/calendar-task-view/', views.CalendarViewNew.as_view(), name='calendar'),
    path('all-event-list/', views.all_events_view, name = "all_events"),
    path('running-event-list/', views.current_events_view, name = "running_events"),
    path('view-client-tasks/', views.view_client_tasks, name ='view-tasks'),
    path('add/task-outfrnt/', views.add_outfrnt_tasks, name = "outfrnt_task"),
    path('view-details-task/<int:event_id>/', views.detail_task_view , name = "task-details"),
    path('delete-task/<str:event_id>/', views.delete_client_task, name = "delete_task_client"),
    path('delete-task-outfrnt/<str:event_id>/', views.delete_outfrnt_task, name = "delete_task_outfrnt"),
]

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as authViews

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('accounts.urls')),
    path('', include('calendarapp.urls')),
    path('', include('questionnaire.urls')),
    
    #password urls 
    path('password_change/done/'
    ,authViews.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html')
    ,name='password_change_done'),

    path('password_change/',
    authViews.PasswordChangeView.as_view(template_name='registration/password_change.html')
    ,name='password_change'
    ),
]

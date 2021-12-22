"""eventcalendar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as authViews

from .views import DashboardView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('calendarapp.urls')),
    
    
    #password urls 
    path('password_change/done/'
    ,authViews.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html')
    ,name='password_change_done'),

    path('password_change/',
    authViews.PasswordChangeView.as_view(template_name='registration/password_change.html')
    ,name='password_change'
    ),

    path('password_reset_done/done/'
    ,authViews.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html')
    ,name='password_reset_done'),

    path('reset/<uidb64>/<token>/'
    ,authViews.PasswordResetConfirmView.as_view()
    ,name='password_reset_confirm'),

    path('password_reset/'
    ,authViews.PasswordResetView.as_view()
    ,name = 'password_reset'),

    path('reset/done/'
    ,authViews.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html')
    ,name ='password_reset_complete'),
]

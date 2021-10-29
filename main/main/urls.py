from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')), # account app urls # calender app urls 
    # calender app urls # calender
]

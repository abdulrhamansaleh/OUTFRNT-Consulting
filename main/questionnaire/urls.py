from django.urls import path

from . import views

app_name = 'questionnaire'

urlpatterns = [
    path('client/sales/form', views.sales_and_management , name = "sales"),
]

from django.urls import path

from questionnaire import views

app_name = 'questionnaire'

urlpatterns = [
    path('new-client/', views.questionnaire_view , name = "main"),
    path('client/sales/form/<int:question_id>', views.sales_and_management , name = "sales"),
    path('client/people/form/<int:question_id>', views.people_and_culture , name = "people"),
    path('client/accounting/form/<int:question_id>', views.accounting_and_finance , name = "accounting"),
    path('client/buisness/form/<int:question_id>', views.buisness_and_operations , name = "buisness"),
    path('client/legal/form/<int:question_id>', views.legal_and_governance , name = "legal"),
    path('client/technology/form/<int:question_id>', views.technology , name = "technology"),
    path('coach/client-questions/', views.questions, name = "questions"),
    path('coach/view-client-responses/<int:client_id>', views.questionnaire_responses , name = "view-response"),
]

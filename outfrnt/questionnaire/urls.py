from django.urls import path

from questionnaire import views

app_name = 'questionnaire'

urlpatterns = [
    path('new-client/', views.questionnaire_view , name = "main"),
    path('client/sales/form/<category>', views.answer_question , name = "answer"),
    path('coach/add-client-questions/', views.add_questions, name = "add-questions"),
    path('coach/view-client-responses/<int:client_id>', views.questionnaire_responses_to_pdf , name = "view-response"),
]

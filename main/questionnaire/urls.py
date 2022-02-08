from django.urls import path

from questionnaire import views

app_name = 'questionnaire'

urlpatterns = [
    path('new-client/', views.questionnaire_view , name = "main"),
    path('client/sales/form/<category>', views.answer_question , name = "answer"),
    path('coach/client-questions/', views.questions, name = "questions"),
    path('coach/view-client-responses/<int:client_id>', views.questionnaire_responses , name = "view-response"),
]

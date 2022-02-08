from django.contrib import admin
from questionnaire import models 

@admin.register(models.Question)
class questionnaireAdmin(admin.ModelAdmin):
    model = models.Question
    list_display = [
        'id',
        'answered',
        'question_text',
        'question_answer',
        'responder',
        'category',
    ]

@admin.register(models.Response)
class reponseAdmin (admin.ModelAdmin):
    model = models.Response
    list_display = [
        'responder', 
        'answer'
    ]
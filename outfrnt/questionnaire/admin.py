from django.contrib import admin
from questionnaire import models 

@admin.register(models.Question)
class questionnaireAdmin(admin.ModelAdmin):
    model = models.Question
    list_display = [
        'id',
        'question_text',
        'category',
    ]

@admin.register(models.Response)
class reponseAdmin (admin.ModelAdmin):
    model = models.Response
    list_display = [
        'responder', 
        'answer'
    ]

@admin.register(models.Questionnaire)
class questionnaireAdmin (admin.ModelAdmin):
    model = models.Questionnaire
    list_display = [
        'question',
        'provided_for',
        'answered'
    ]

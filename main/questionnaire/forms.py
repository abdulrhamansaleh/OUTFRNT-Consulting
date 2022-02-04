from django.forms import ModelForm
from questionnaire.models import Question,Response
from django import forms

class AnswerForm(ModelForm):
    class Meta: 
        model = Response 
        fields = ['answer']  
        widgets = {
        'answer': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Response to question',
                'rows':10,
                'style':'resize:none;'
            }),
    }

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

class AddQuestions(ModelForm):
    class Meta:
        model = Question 
        fields = ['question_text','category']
        widgets = {
            'question_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ''
            })
        }
        exclude = ['responder','question_answer']
    def __init__(self, *args, **kwargs):
        super(AddQuestions, self).__init__(*args, **kwargs)
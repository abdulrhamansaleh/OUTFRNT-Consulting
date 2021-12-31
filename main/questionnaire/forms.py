from django.forms import ModelForm,forms
from models import OutfrntQuestion
class Questionnaire(ModelForm):
    answer = forms.CharField(max_length=255)
    class Meta:
        model = OutfrntQuestion
        fields = ('question','answer')


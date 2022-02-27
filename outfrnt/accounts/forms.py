from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text="Required",widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))
    username = forms.CharField(max_length=30,help_text="Required",widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    
    class Meta:
        model = User
        fields = ('email','username','password1','password2')


class JoinUs(forms.Form):
    first_name = forms.CharField(
    label = "First Name", max_length = 100,
    widget = forms.TextInput(
        attrs = {
            'class':'form-control',
            'placeholder':'First Name',
        }
    )
    )
    last_name = forms.CharField(
        label = "Last Name",
        max_length = 100,
        widget = forms.TextInput(
        attrs = {
            'class':'form-control',
            'placeholder':'Last Name',
        }
    )
    )
    email = forms.EmailField(
        max_length = 254,
        widget = forms.EmailInput(
        attrs = {
            'class':'form-control',
            'placeholder':'Email Address',
        }
    )
    )
    phone_num = forms.IntegerField(
        min_value = 1,
        widget = forms.NumberInput(
            attrs = {
                'class':'form-control',
                'placeholder':'Phone Number'
            }
        )
    )
    help_body = forms.CharField(
        widget = forms.Textarea(
            attrs = {
                'class':'form-control',
                'placeholder':'How can we help ?',
                'rows':12,
                'cols':22,
                'style':'resize:none',
            }
        ) 
    )

    
    
    
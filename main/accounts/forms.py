from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserAccount
from django.forms import ModelForm, DateInput
from django import forms

class registerForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text="Required")
    class Meta:
        model = UserAccount
        fields = ('email','username','password1','password2')

class loginForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    class Meta:
        model = UserAccount
        fields = ('email','password')
    
    def clean(self):
        if self.is_valid:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Email or Password")

class UpdateAccountForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ('email','username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = UserAccount.objects.exclude(pk=self.instance.pk).get(email=email)
            except UserAccount.DoesNotExist:
                return email
            raise forms.ValidationError(f'{email} is already in use')

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = UserAccount.objects.exclude(pk=self.instance.pk).get(username=username)
            except UserAccount.DoesNotExist:
                return username
            raise forms.ValidationError(f'{username} is already in use')

from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from accounts.forms import SignInForm,SignUpForm,UpdateAccountForm
from calendarapp.models import Event
from accounts.models import User 

def home(request):
    return render(request,'main.html')

def signout(request):
    logout(request)
    return redirect('accounts:home')

def profileView(request):
    # make sure profile can only be visited by authenticated and logged users 
    if not request.user.is_authenticated:
        return redirect('accounts:signin')

    variables = {}

    if request.POST:
        form = UpdateAccountForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            if request.user.is_coach:
                return render(request,'calendarapp/coachPortal.html')
        return render(request,'calendarapp/calendar.html')
    else:
        form = UpdateAccountForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
        
    variables['profile'] = form
    return render (request,'accounts/profile.html',variables)

class SignInView(View):
    def get(self, request, *args, **kwargs):
        forms = SignInForm
        variables = {
            'form': forms
        }
        return render(request,'accounts/signin.html', variables)

    def post(self, request, *args, **kwargs):
        forms = SignInForm(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data['email']
            password = forms.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if request.user.is_coach:
                    return render(request,'coach/coachPortal.html',)
                else:
                    return render(request,'calendarapp/calendar.html')
        variables = {
            'form': forms
        }
        return render(request, 'accounts/signin.html', variables)

class SignUpView(View):
    form_class = SignUpForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {
            'form': forms
        }
        return render(request,'accounts/signup.html', context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('accounts:signin')
        context = {
            'form': forms
        }
        return render(request,'accounts/signup.html', context)

def coachView(request):
    clients = User.objects.all()
    tasks = Event.objects.all()
    variables = {
        'users':clients,
        'tasks':tasks,
    }
    return render(request,'coach/viewClients.html',variables)

   
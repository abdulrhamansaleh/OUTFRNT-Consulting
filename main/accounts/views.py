# django imports 
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# python imports 
import datetime 
# app imports 
from accounts.forms import SignInForm,SignUpForm,JoinUs
from accounts.models import User
from questionnaire.models import Question

# landing page with connection form 
def home(request):
    form = JoinUs(request.POST or None)
    variables = {
        "form":form
    }
    if 'join' in request.POST:
        print("posting data")
        if form.is_valid():
            print("form is valid")
            first = form.cleaned_data["first_name"]
            last = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone_num"]
            help_body = form.cleaned_data["help_body"]
            variables = {
                "first":first,
                "last":last,
                "email":email,
                "phone":phone,
                "body":help_body,
            }
            return redirect('accounts:home')
    form = JoinUs
    return render(request,'landing.html',variables)
    
class SignInView(View):
    def get(self, request, *args, **kwargs):
        variables = {
            'form': SignInForm
        }
        return render(request,'accounts/signin.html', variables)

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                if user.is_newclient:
                    return redirect("questionnaire:main")
                else:
                    return redirect('accounts:home')
        variables = {
            'form': form,
        }
        return render(request, 'accounts/signin.html', variables)

class SignUpView(View):
    def get(self, request, *args, **kwargs):
        variables = {
            'form': SignUpForm
        }
        return render(request,'accounts/signup.html', variables)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:signin')
        variables = {
            'form': form
        }
        return render(request,'accounts/signup.html', variables)

@login_required(login_url = '/signin/')
def signout(request):
    logout(request)
    return redirect('accounts:home')

@login_required(login_url = '/signin/')
def remove_user(request,client):
    if request.user.is_coach:
        User.objects.filter(username = client).delete()
        return redirect('accounts:manage')
    else:
        return home(request)
    
# Management Panel for authorized coaches 
@login_required(login_url = '/signin/')
def manage_clients_status(request):
    if request.user.is_coach:
        variables = {
            "newclients": User.objects.filter(is_newclient = True),
            "clients": User.objects.filter(is_client = True),
            "prospects": User.objects.filter(is_prospect = True),
        }
        return render(request,'coach/manageusers.html', variables)
    else:
        return home(request)

@login_required(login_url = '/signin/')
def update_status_to_client(request,user):
    if request.user.is_coach:
        User.objects.filter(username = user).update(
            is_newclient = False,
            is_prospect = False,
            is_client = True
        )
        return redirect('accounts:manage')
    else:
        return home(request)

@login_required(login_url = '/signin/')
def update_status_to_newclient(request,client):    
    client = User.objects.filter(username = client)
    if request.user.is_coach:
        subject_of_email = "Welcome to OUTFRNT"
        email_body = "Thank you for choosing OUTFRNT. Knowing you and your business is quintessential to how we can help you. Your online access to OUTFRNT.com gives you the option to complete our client survey at your convenience. Alternatively, one of our business advisors can complete this with you."
        email_sender = "pureexec@gmail.com"
        clients_of_interest = [f'{client[0].email}']

        #send_mail(
            #subject_of_email,
            #email_body,
            #email_sender,
            #clients_of_interest,
            #fail_silently = False
        #)
        
        client.update(
            is_newclient = True,
            is_prospect = False,
            is_client = False,
            completed_P1 = False,
            completed_P2 = False,
            completed_P3 = False,
            completed_P4 = False,
            completed_P5 = False,
            completed_P6 = False,
        )
        return redirect('accounts:manage')
    else:
        return home(request)

@login_required(login_url = '/signin/')
def update_status_to_prospect(request,client):
    if request.user.is_coach:
        User.objects.filter(username = client).update(
            is_newclient = False,
            is_client = False,
            is_prospect = True,
            completed_P1 = False,
            completed_P2 = False,
            completed_P3 = False,
            completed_P4 = False,
            completed_P5 = False,
            completed_P6 = False,
        )
        return redirect('accounts:manage')
    else:
        return home(request)

        
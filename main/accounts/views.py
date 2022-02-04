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
from accounts.forms import SignInForm,SignUpForm
from calendarapp.models import Event
from accounts.models import User
from questionnaire.models import Question

def home(request):
    return render(request,'main.html')

# signout users
@login_required(login_url = '/signin/')
def signout(request):
    logout(request)
    return redirect('accounts:home')

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
def view_client_tasks(request):
    if request.user.is_coach:
        clients = User.objects.all()
        tasks = Event.objects.all()
        
        if 'search-key' in request.GET:
            search = request.GET['search-key']
            variables = {
                'users': User.objects.filter(username = search),
                'tasks':tasks
            }
            return render(request,'coach/viewClients.html', variables)
        else:
            variables = {
            'users': clients,
            'tasks':tasks,
            }
        return render(request,'coach/viewClients.html', variables)
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
        return render(request,'coach/manage.html', variables)
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
        # After becoming a new client email user to let them know there is a questionnaire they must fill out 
        subject_of_email = "Let us know more about your buisness"
        email_body = f'Welcome {client[0].username}, login to OUTFRNT to access your questionnaire'
        email_sender = "pureexec@gmail.com"
        clients_of_interest = [f'{client[0].email}']

        # debug line python -m smtpd -n -c DebuggingServer localhost:1011
        # send_mail(
        #    subject_of_email,
        #    email_body,
        #    email_sender,
        #    clients_of_interest,
        #    fail_silently = False
        #)
        
        # update user access and progress for enrollement
        client.update(
            is_newclient = True,
            is_prospect = False,
            is_client = False,
            categories_answered = 0,
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
            categories_answered = 0, 
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
def remove_user(request,client):
    if request.user.is_coach:
        User.objects.filter(username = client).delete()
        return redirect('accounts:manage')
    else:
        return home(request)
        
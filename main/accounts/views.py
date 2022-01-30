from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from accounts.forms import SignInForm,SignUpForm
from calendarapp.models import Event
from accounts.models import User
from questionnaire.models import Question
from django.contrib import messages 
import datetime 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

def home(request):
    return render(request,'main.html')

# signout users
@login_required(login_url = 'accounts/signin.html')
def signout(request):
    logout(request)
    return redirect('accounts:home')
class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm
        variables = {
            'form': form
        }
        return render(request,'accounts/signin.html', variables)

    def post(self, request, *args, **kwargs):
        questions = Question.objects.all()
        users = User.objects.all()
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
        form = SignUpForm
        variables = {
            'form': form
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
    
@login_required(login_url = 'accounts/signin.html')    
def view_client_tasks(request):
    if request.user.is_coach:
        clients = User.objects.all()
        tasks = Event.objects.all()
        
        if 'search-key' in request.GET:
            search = request.GET['search-key']
            clients = User.objects.filter(username = search)
            variables = {
                'users':clients,
                'tasks':tasks
            }
            return render(request,'coach/viewClients.html', variables)
        else:
            variables = {
            'users':clients,
            'tasks':tasks,
            }
        return render(request,'coach/viewClients.html', variables)
    else:
        return home(request)
    

# Admin Panel
@login_required(login_url = 'accounts/signin.html')
def manage_clients_status(request):
    if request.user.is_coach:
        # add questionnaire logic here 
        users = User.objects.all()
        clients = User.objects.filter(is_coach = False , is_admin = False)
        newclients = User.objects.filter(is_newclient = True)
        coaches = User.objects.filter(is_coach = True)
        prospects = User.objects.filter(is_prospect = True)
        variables = {
            "newclients":newclients,
            "clients":clients,
            "coaches":coaches,
            "prospects":prospects,
        }
        return render(request,'coach/manage.html', variables)
    else:
        return home(request)

@login_required(login_url = 'accounts/signin.html')
def update_status_to_client(request,user):
    if request.user.is_coach:
        client = User.objects.filter(username = user)
        client.update(
            is_newclient = False,
            is_prospect = False,
            is_client = True
        )
        return redirect('accounts:manage')
    else:
        return home(request)

@login_required(login_url = 'accounts/signin.html')
def update_status_to_newclient(request,client):    
    if request.user.is_coach:
        client = User.objects.filter(username = client)
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

@login_required(login_url = 'accounts/signin.html')
def update_status_to_prospect(request,client):
    if request.user.is_coach:
        client = User.objects.filter(username = client)
        client.update(
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

@login_required(login_url = 'accounts/signin.html')    
def remove_user(request,client):
    if request.user.is_coach:
        user = User.objects.filter(username = client)
        user.delete()
        return redirect('accounts:manage')
    else:
        return home(request)
        
# django imports 
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# app imports 
from accounts.forms import SignInForm,SignUpForm,JoinUs
from accounts.models import User

# landing page with connection form 
def home(request):
    # request user 
    user = request.user 
    # join us form 
    form = JoinUs(request.POST or None)
    # context for html page 
    variables = {
        "form":form
    }
    # return registered users to respective portals 
    if  user.is_authenticated:
        # send user to survey 
        if user.is_newclient:
            return redirect('questionnaire:main')
        # send user to calendar 
        elif user.is_client:
            return redirect('calendarapp:dashboard')
        elif user.is_coach:
        # send user to coach/admin type portal 
            return redirect('calendarapp:view-tasks')
        # keep user in landing page 
        else:
            return redirect('accounts:home')
    # for users interested in OUTFRNT services 
    if not user.is_authenticated:
        # if join form is populated with values 
        if 'join' in request.POST:
            if form.is_valid():
                # retrieve values from form 
                first = form.cleaned_data["first_name"]
                last = form.cleaned_data["last_name"]
                email = form.cleaned_data["email"]
                phone = form.cleaned_data["phone_num"]
                help_body = form.cleaned_data["help_body"]
                # send an email to no-reply company mail for employees to screen interested clients 
                send_mail(
                    'OUTFRNT CONTACT FORM: Verify For Possible Spam',
                    f'Name: {first} {last}\nPhone: {phone}\nEmail: {email}\nInquiry: {help_body}',
                    'pureexec@gmail.com',# Deployment 'noreply@outfrnt.com'
                    ['pureexec@gmail.com'],# Deployment 'noreply@outfrnt.com'
                    fail_silently = False
                )
            # return users back to home page after sumbitting the form 
            return redirect('accounts:home')
    # initial render of home page 
    return render(request,'landing.html',variables)

# sign in view  
class SignInView(View):
    # get method to retrieve form fields 
    def get(self, request, *args, **kwargs):
        variables = {
            'form': SignInForm
        }
        # render sign in page with context data 
        return render(request,'accounts/signin.html', variables)

    # post method to attempt a sign in 
    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            # retrieve values from form 
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            # attempt to authenticate user
            user = authenticate(email = email, password = password)
            # if user is valid in the system identify next endpoint for user depending on permissions 
            if user:
                # authenticate user 
                login(request, user)
                # send user to survey 
                if user.is_newclient:
                    return redirect('questionnaire:main')
                # send user to calendar 
                elif user.is_client:
                    return redirect('calendarapp:dashboard')
                elif user.is_coach:
                # send user to coach/admin type portal 
                    return redirect('calendarapp:view-tasks')
                # keep user in landing page 
                else:
                    return redirect('accounts:home')
        # context for html page 
        variables = {
            'form': form,
        }
        # render for post data 
        return render(request, 'accounts/signin.html', variables)

# sign up view 
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        # get form fields to populate 
        variables = {
            'form': SignUpForm
        }
        # render for get data 
        return render(request,'accounts/signup.html', variables)

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            # save user registration data 
            form.save()
            # allow user to sign in after registry 
            return redirect('accounts:signin')
        # context for html page 
        variables = {
            'form': form
        }
        return render(request,'accounts/signup.html', variables)

# signout functionality 
@login_required(login_url = '/signin/')
def signout(request):
    logout(request)
    return redirect('accounts:home')

# MANAGEMENT PANEL

# main page to show all user permissions 
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

# MANAGEMENT FUNCTIONALITIES

# update a new client to client status 
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

# revoke client membership from existing client or update prospect to new client 
@login_required(login_url = '/signin/')
def update_status_to_newclient(request,client):    
    client = User.objects.filter(username = client)
    # check if user has authentication to access this managerial based endpoint
    if request.user.is_coach:
        # check if new client was a prospect to provide an email notifying them  
        if client.is_prospect:     
            # content for email 
            subject_of_email = "Welcome to OUTFRNT"
            email_body = "Thank you for choosing OUTFRNT.\n\tKnowing you and your business is quintessential to how we can help you. Your online access to OUTFRNT.com gives you the option to complete our client survey at your convenience. Alternatively, one of our business advisors can complete this with you."
            email_sender = "pureexec@gmail.com"# deployment noreply@outfrnt.com
            clients_of_interest = ['pureexec@gmail.com']# deployment f'{client[0].email}'
            # send email 
            send_mail(
                subject_of_email,
                email_body,
                email_sender,
                clients_of_interest,
                fail_silently = False
            )
        # update status either way 
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
        # return to managemnet end point
        return redirect('accounts:manage')
    # return user to home if they try to access an unauthorized endpoint
    else:
        return home(request)


# revoke user to initial registration point , cannot access either client survery or client calendar
@login_required(login_url = '/signin/')
def update_status_to_prospect(request,client):
    # check if user has authority to access this endpoint 
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
    # return user to home if they try to access an unauthorized endpoint
    else:
        return home(request)

# remove user from database 
@login_required(login_url = '/signin/')
def remove_user(request,client):
    # check if user has authority to access this endpoint 
    if request.user.is_coach:
        # remove user and any related info from the database 
        User.objects.filter(username = client).delete()
        return redirect('accounts:manage')
     # return user to home if they try to access an unauthorized endpoint
    else:
        return home(request)
    
        
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from accounts.forms import registerForm,loginForm,UpdateAccountForm

def home(request):
    return render(request,'main.html')
# logout view for any user to logout of their account 
def logoutUser(request):
    logout(request)
    return render(request,'main.html')
    
# login page for users 
def loginUser(request):
    variables = {}
    # user varaible reference
    user = request.user
    if user.is_authenticated and user.is_coach:
        return render(request,'accounts/coachportal.html')
    if request.POST:
        form = loginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            account = authenticate(email=email, password=password)
        if user:
            login(request,account)
            return render(request,'main.html')
            #return redirect('home')
    # if the user sumbits no fields  
    else:
        form = loginForm()
        variables['login_form'] = form
        return render(request, 'accounts/login.html',variables)



# register page for clients 
def registerClient(request):
    client = request.user
    if client.is_authenticated:
        return render(request,'main.html')
    else:
        # registeration form from django library
        variables = {}
        if request.POST:
            # pass in form data
            form = registerForm(request.POST)
            # check if form is valid (no form issues)
            if form.is_valid():
                form.save();
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                # authenticate user
                clientAccount = authenticate(email= email,password = raw_password)
                login(request, clientAccount)
                # return them to the calender view 
                return render(request,'main.html')
            else:
                variables['form'] = form
        # any variables for data that the registration page needs to render
        else: # get request
            form = registerForm() 
            variables['form'] = form
        return render(request,'accounts/register.html',variables)

# account view to edit information 
def profileView(request):
    # make sure profile can only be visited by authenticated and logged users 
    if not request.user.is_authenticated:
        return redirect('login')

    variables = {}

    if request.POST:
        form = UpdateAccountForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            # return them to the calender view 
        return render(request,'main.html')
    else:
        form = UpdateAccountForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )

    variables['profile'] = form
    return render (request,'accounts/profile.html',variables)


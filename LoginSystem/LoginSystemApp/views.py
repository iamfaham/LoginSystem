from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render (request, 'home.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username = username, password = pass1)

        if user is not None:
            login(request,user)
            return redirect ('homepage')
        else:
            messages.error(request, 'Username or password incorrect!')
            

    return render (request, 'loginpage.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1!=pass2:
            messages.error(request, 'Passwords do not match!')
        elif len(pass1) < 8:
            messages.error(request, 'Password should be atleast 8 characters!')
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            messages.success(request, 'Account created successfully!!')
            return redirect('loginpage')
           
    return render (request, 'signup.html')

@login_required(login_url='loginpage')
def homepage(request):
    return render (request, 'homepage.html')

def logoutpage(request):
    logout(request)
    return redirect('loginpage')
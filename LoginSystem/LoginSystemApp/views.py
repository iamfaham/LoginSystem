from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import cache_control

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
        request.session["username"] = uname
        request.session["password"] = pass1
        request.session["email"] = email
        if pass1!=pass2:
            messages.error(request, 'Passwords do not match!')
        elif len(pass1) < 8:
            messages.error(request, 'Password should be atleast 8 characters long!')
        else:
            # my_user = User.objects.create_user(uname, email, pass1)
            # my_user.save()
            sendotp(request)
            # messages.success(request, 'Account created successfully!!')
            return redirect('otpverify')
           
    return render (request, 'signup.html')

@login_required(login_url='loginpage')  # if someone enter the url name of page which appears after login, this will prevent it and requires user to login first
@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # press back button and it will not login again.
def homepage(request):
    return render (request, 'homepage.html')

def logoutpage(request):
    logout(request)
    return redirect('loginpage')

def sendotp(request):
    otp = ""
    for i in range(0,4):
        otp += str(random.randint(0,9))
    request.session["otp"] = otp
    send_mail("Hey " + request.session['username'], "Your OTP for signup is " + otp, "djangootptesting@gmail.com", [request.session['email']], fail_silently=False)
    return render (request , 'otp.html')

def otpverify(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == request.session['otp']:
            encryptedpass = make_password(request.session['password'])
            user = User(username = request.session['username'], email = request.session['email'], password = encryptedpass)
            user.save()
            messages.success(request, 'OTP verification successful')
            return redirect('loginpage')

        else:
            messages.error(request, 'Incorrect OTP, please try again.')
            return render (request, 'otp.html')
    return render (request, 'otp.html')
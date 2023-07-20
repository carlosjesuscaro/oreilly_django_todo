from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def signupuser(request):
    if request.method == 'GET':
        return render(request, "signupuser.html", {'form': UserCreationForm()})
    else:
        # Create a user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current')
            except IntegrityError:
                return render(request, "signupuser.html", {'form': UserCreationForm(),
                                                           'error': 'Username already exists'})
        else:
            return render(request, "signupuser.html", {'form': UserCreationForm(),
                                                       'error': 'Passwords do not match'})


def current(request):
    return render(request, "current.html")


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, "login.html", {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form': AuthenticationForm(),
                                                  'error': "Username and password do not match"})
        else:
            login(request, user)
            return redirect('current')

def home(request):
    return render(request, "home.html")

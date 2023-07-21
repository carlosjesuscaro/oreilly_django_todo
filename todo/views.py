from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone


def signup_user(request):
    if request.method == 'GET':
        return render(request, "signup.html", {'form': UserCreationForm()})
    else:
        # Create a user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('current')
            except IntegrityError:
                return render(request, "signup.html", {'form': UserCreationForm(),
                                                       'error': 'Username already exists'})
        else:
            return render(request, "signup.html", {'form': UserCreationForm(),
                                                   'error': 'Passwords do not match'})


def current(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, "current.html", {'todos': todos})


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def login_user(request):
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


def create_todo(request):
    if request.method == 'GET':
        return render(request, "create.html", {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current')
        except ValueError:
            return render(request, "create.html", {'form': TodoForm(), 'error': "Incorrect entry"})


def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form_todo = TodoForm(instance=todo)
        return render(request, "view_todo.html", {'todo': todo, 'form': form_todo})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, "view_todo.html", {'todo': todo,
                                                      'form': TodoForm(request.POST, instance=todo),
                                                      'error': "Bad information"})


def test(request):
    return render(request, "test.html")


def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect("current")

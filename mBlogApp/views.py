from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegistrationForm, LoginForm, CreatePostForm
from .models import Post

def welcome(request):
    return render(request, 'welcome.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(username= form.cleaned_data['username'],
                                     password= form.cleaned_data['password'])
            messages.add_message(request, messages.SUCCESS, "You may now log in")
            return redirect('login')
    else :
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form, 'show_valid': True})    

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username= username, password= password)

            if user is not None:
                messages.add_message(request, messages.SUCCESS, "Welcome back!")
                return redirect('welcome')
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'show_valid': False})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages

from .forms import RegistrationForm, LoginForm, CreatePostForm
from .models import Post
from .apps import MblogappConfig
from .utils import *

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
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, "Welcome back!")
                return redirect('feed')
            else:
                messages.add_message(request, messages.ERROR, "Invalid Credentials")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'show_valid': False})

def feed(request):
    posts = Post.objects.all().order_by('-date_posted')

    # read up on what exactly request.POST is
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            song     =  form.cleaned_data['song']
            artist   = form.cleaned_data['artist']
            content  = form.cleaned_data['content']
            client = MblogappConfig.client
            filename = download_image(client.get_first_track_album_image_url(song, artist))
            
            post     = Post(title= song, artist = artist, content= content,
                            author= User.objects.get(username= request.user.username),
                            albumart= filename)
            post.save()

    form = CreatePostForm()
    return render(request, 'feed.html', {'posts': posts, 'form': form})

def logout(request):
    auth_logout(request)
    return redirect('welcome')

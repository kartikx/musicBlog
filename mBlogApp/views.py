from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

from .forms import RegistrationForm, LoginForm, CreatePostForm
from .models import Post, Genre
from .apps import MblogappConfig
from .utils import *

def welcome(request):
    if request.user.is_authenticated:
        return redirect('feed')
    return render(request, 'welcome.html')

def register(request):
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "You're already Logged in.")
        return redirect('feed')
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
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "You're already Logged in.")
        return redirect('feed')

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
    if not request.user.is_anonymous:
        liked_posts = request.user.liked_posts.all()
        liked_posts_ids = [post.id for post in liked_posts]
    else:
        liked_posts_ids = []

    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            createAndSavePost(request, form)
            return redirect('feed')

    form = CreatePostForm()
    return render(request, 'feed.html', {'posts': posts, 'form': form , 'liked_posts': liked_posts_ids})

def genre(request, genrename):
    if not request.user.is_anonymous:
        liked_posts = request.user.liked_posts.all()
        liked_posts_ids = [post.id for post in liked_posts]
    else:
        liked_posts_ids = []

    genrename = " ".join(genrename.split('-'))

    try:
        genre = Genre.objects.get(name__iexact=genrename)
    except Genre.DoesNotExist:
        return HttpResponse(status=400)
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            createAndSavePost(request, form)
            return redirect('feed')

    # Get songs which contain the genre.
    posts = Post.objects.filter(genres__id = genre.id).order_by('-date_posted')
    form = CreatePostForm()

    return render(request, 'genre.html', {'genre': genre , 'posts': posts, 'form': form, 'liked_posts': liked_posts_ids})


def createAndSavePost(request, form):
    song     =  form.cleaned_data['song']
    artist   = form.cleaned_data['artist']
    content  = form.cleaned_data['content']
    client   = MblogappConfig.client
    filename = download_image(client.get_first_track_album_image_url(song, artist))
    genres   = client.get_genre_for_track(song, artist)
    spotifylink = client.get_spotify_link(song, artist)
    post     = Post(title= song, artist = artist, content= content,
                    author= User.objects.get(username= request.user.username),
                    albumart= filename, spotifylink= spotifylink)
    post.save()
    
    for genre in genres:
        genre_instance = Genre.objects.filter(name= genre).first()
        if genre_instance is None :
            post.genres.create(name= genre)
        else :
            post.genres.add(genre_instance)
    post.save()

def logout(request):
    auth_logout(request)
    return redirect('welcome')

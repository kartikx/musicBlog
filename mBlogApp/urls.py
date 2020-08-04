from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('feed/', views.feed, name='feed'),
    path('logout/', views.logout, name='logout'),
    path('genre/<slug:genrename>/', views.genre, name='genre'),
]

# Currently doing genre via the primary key, might try to switch to the genre name instead? - separated?

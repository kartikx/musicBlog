from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('about/', views.about, name='about'),
    path('explore/', views.explore, name='explore'),
    path('community/', views.community, name='community'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('feed/', views.feed, name='feed'),
    path('logout/', views.logout, name='logout'),
    path('user/<str:username>/', views.profile, name='profile'),
    path('genre/<slug:genrename>/', views.genre, name='genre'),
]

handler500 = views.handler500

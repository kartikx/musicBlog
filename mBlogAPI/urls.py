from django.urls import path
from . import views

# FIX these to have all terminal /
urlpatterns = [
    path('posts-list', views.postsList, name='posts-list'),
    path('post-details/', views.postDetails, name='post-details-default'),
    path('post-details/<int:pk>', views.postDetails, name='post-details'),
    path('post-details/<int:pk>/<str:action>', views.postDetailsAction, name='post-details-action'),
    path('posts-liked/<int:pk>/', views.postsLiked, name='posts-liked'),
]
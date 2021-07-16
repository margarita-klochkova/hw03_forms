from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.new_post, name='new_post'),
    path('<str:username>/<int:post_id>/edit/',
         views.post_edit, name="post_edit"),
    path("", views.index, name="index"),
    path("group/<slug:slug>/", views.posts_group, name="posts_group"),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post')]

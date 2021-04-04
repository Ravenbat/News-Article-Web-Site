from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'), 
    path('about', about, name='about'),
    path('login', user_login, name='login'),
    path('posts/<int:id>', posts, name='posts'),
    path('register', user_register, name='register'),
    path('post/create', create_post, name='create-post'),
    path('posts/mine', myposts, name='my-posts'),
    path('logout', user_logout, name='logout'),
    path('post/<int:id>', post, name='post'),
    path('comment/create/<int:id>', create_comment, name='comment'),
    path('post/comment/update/<int:id>', editComment)
]
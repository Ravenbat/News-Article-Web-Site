from django.shortcuts import render, redirect
import json
from django.http import HttpResponse, JsonResponse
from .models import Post, Category, Comment, User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from .forms import CreatePostForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@login_required(login_url='login')
def home(request):
    context = {
        'catergory_list': Category.objects.all(),
        'posts': Post.objects.all().order_by('-created_at')
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')
def about(request):
    context = {
        'catergory_list': Category.objects.all()
    }
    return render(request, 'about.html', context)

def hello(request):
    return HttpResponse('Hello django')

@login_required(login_url='login')
def posts(request, id):
    data = Post.objects.filter(Category__id=id).order_by('-created_at')
    catergory = Category.objects.all()
    context = {
        'posts': data,
        'cnt': len(data),
        'catergory_list': catergory
    }
    return render(request, 'posts.html', context)

def user_login(request):
    if request.method == 'POST':
        user_data = AuthenticationForm(data=request.POST)
        if user_data.is_valid():
           user = user_data.get_user()
           login(request, user)
           return redirect('home')
        else:
           return redirect('home')
    else:
        context = {
        'form': AuthenticationForm()
    }
    return render(request, 'user-login.html', context)

def user_register(request):
    if request.method == "POST":
       form_data = UserCreationForm(request.POST)
       if form_data.is_valid():
           user = form_data.save()
           login(request, user)
           return redirect('home')
       else:
           return redirect('register')
    else: 
        context = {
            'form': UserCreationForm()
        }
    return render(request, 'user_register.html', context)
    
def user_logout(request):
    logout(request)
    return redirect('login')

def post(request, id):
    context={
        'post': Post.objects.get(id=id),
        'catergory_list': Category.objects.all(),
        'comments' : Comment.objects.filter(post__id = id).order_by('-created_at'),
    }
    return render(request, 'post.html', context)

def create_comment(request, id):
    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.text = request.POST['commenttext']
        comment.post = Post.objects.get(id=id)
        comment.save()
        return redirect('post', id)
    else:
        return redirect('pass', id)

def create_post(request):
    if request.method == 'POST':
        post = CreatePostForm(data=request.POST)
        if post.is_valid():
            new_post = post.save(commit=False)
            new_post.author = request.user
            new_post.image = request.FILES['image']
            new_post.save()
            return redirect('home')
        else:
            return redirect('create-post')
    else:
        context = {
            'catergory_list': Category.objects.all(),
            'form': CreatePostForm()
        }
        return render(request, 'post-create.html', context)

def myposts(request):
    currentuser = request.user
    currentuser_id = User.objects.get(username=currentuser).id
    myposts = Post.objects.filter(author = currentuser)
    return render(request, "myposts.html", context={
        "myposts": myposts,
        "catergory_list" : Category.objects.all()
    })
@csrf_exempt
def editComment(request, id):
    if request.user.is_authenticated:
        current_user = request.user
    else:
        return HttpResponse("You must be logged in to try to do that.")

    if request.method == "PUT":
        comment = Comment.objects.get(id=id)
        if comment.user_id == current_user.id:
            data = json.loads(request.body)
            newComment = data.get("newComment")
            comment.text = newComment
            comment.save()
            return JsonResponse(comment.serialize())
        else:
            return HttpResponse("Access denied.")
    else:
        return HttpResponse("Access denied.")


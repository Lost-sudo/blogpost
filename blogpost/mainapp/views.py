from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUser, PostForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post, Comment

# Create your views here.

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is incorrect")

    context = {}
    return render(request, 'mainapp/login.html', context)

def signuppage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUser

        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect('login')
    
    context = {'form':form}
    return render(request, 'mainapp/signup.html', context)

@login_required(login_url='login')
def homepage(request):
    posts = Post.objects.all()
    return render(request, 'mainapp/home.html', {'posts': posts})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def postpage(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('profile')
    else:
        form = PostForm()
    return render(request, 'mainapp/post.html', {'form': form})

@login_required(login_url='login')
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', slug=slug)
    else:
        comment_form = CommentForm()
    return render(request, 'mainapp/post_detail.html', {
        'post': post,
        'comments':comments,
        'comment_form':comment_form,
        })

@login_required(login_url='login')
def profilepage(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'mainapp/profile.html', {'posts': user_posts})

@login_required(login_url='login')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('profile')
    else:
        return redirect('home')
    
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = PostForm(instance=post)
        return render(request, 'mainapp/post_update.html', {'form':form})
    else:
        return redirect('home')

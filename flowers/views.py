from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
	return render(request, "index.html")

def dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "all_posts": Post.objects.all().order_by("-updated_at"),
            "logged_user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, "dashboard.html", context)

def new(request):
    context = {
        "logged_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "addPost.html", context)

def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash
        )
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def login(request):
    result = User.objects.filter(email=request.POST['login_email'])
    if len(result) > 0:
        logged_user = result[0]

        if bcrypt.checkpw(request.POST['login_pw'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/dashboard')
        else: 
            messages.error(request, "Email and password did not match.")
    else:
        messages.error(request, "Email has not been registered.")

    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def create(request):
    errors = Post.objects.validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/posts/new')
    else:
        Post.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            content=request.POST['content'],
            posted_by=User.objects.get(id=request.session['user_id'])
        )
        return redirect('/dashboard')

def edit(request, id):
    context = {
        "post": Post.objects.get(id=id),
        "logged_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "editPost.html", context)

def update(request, id):
    errors = Post.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/posts/edit')
    else:
        post = Post.objects.get(id=id)
        post.title=request.POST['title']
        post.description = request.POST['description']
        post.content = request.POST['content']
        post.save()

        return redirect('/dashboard')

def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('/dashboard')

def save(request, id):
    post = Post.objects.get(id=id)
    post.collection.add(User.objects.get(id=request.session['user_id']))
    return redirect('/collection')

def unsave(request, id):
    post = Post.objects.get(id=id)
    post.collection.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/collection')

def show_collection(request,id):
    context = {
        "collection": User.objects.has_collected.all(),
        "logged_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "collection.html", context)

def show_logged_user_posts(request,id):
    context = {
        "my_posts": User.objects.has_posts.all(),
        "logged_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "my_posts.html", context)

def show_post(request, id):
    context = {
        "post": Post.objects.get(id=id),
        "logged_user": User.objects.get(id=request.session['user_id'])
    }
    return render(request, "show_post.html", context)
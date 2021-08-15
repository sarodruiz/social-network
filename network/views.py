import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Post, User

@csrf_exempt
def index(request):
    if request.method != "POST":
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        
        if request.GET.get("page") != None:
            num_page = request.GET.get("page")
        else:
            num_page = 1

        p = Paginator(posts, 10)
        page = p.page(num_page)
        
        return render(request, "network/index.html", {
            "num": int(num_page),
            "page": page,
            "num_pages": range(1, p.num_pages+1),
            "last_page": num_page
        })
    
    data = json.loads(request.body)
    user = request.user
    content = data.get("content", "")
    post = Post(user=user, content=content)
    post.save()

    return JsonResponse({"message": "Post submitted successfully."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, name):
    user = User.objects.get(username=name)
    posts = user.posts.all()
    posts = posts.order_by("-timestamp").all()

    if request.GET.get("page") != None:
        num_page = request.GET.get("page")
    else:
        num_page = 1

    p = Paginator(posts, 10)
    page = p.page(num_page)
        
    return render(request, "network/profile.html", {
        "profile": user,
        "num": int(num_page),
        "page": page,
        "num_pages": range(1, p.num_pages+1),
        "last_page": num_page
    })

    return render(request, "network/profile.html", {
        "profile": user,
        "posts": posts
    })

@login_required
def follow(request, name):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        target = User.objects.get(username=name)
        if target.followers.filter(username=user.username).exists():
            target.followers.remove(user)
        else:
            target.followers.add(user)
        target.save()
    return profile(request, name)

def following(request):
    user = User.objects.get(username=request.user.username)
    following = user.following.all()
    posts = []
    for post in Post.objects.all().order_by("-timestamp"):
        if post.user in following:
            posts.append(post)

    if request.GET.get("page") != None:
        num_page = request.GET.get("page")
    else:
        num_page = 1

    p = Paginator(posts, 10)
    page = p.page(num_page)
        
    return render(request, "network/following.html", {
        "num": int(num_page),
        "page": page,
        "num_pages": range(1, p.num_pages+1),
        "last_page": num_page
    })

    return render(request, "network/following.html", {
            "posts": posts
    })
    #return JsonResponse([post.serialize() for post in posts], safe=False)

@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        data = json.loads(request.body)
        post_id = data.get("id")
        post = Post.objects.get(pk=post_id)
        if user in post.likes.all():
            text = "Like"
            post.likes.remove(user)
        else:
            text = "Dislike"
            post.likes.add(user)
        post.save()
        return JsonResponse({
            "likes": post.likes.count(),
            "text": text
            })

@login_required
@csrf_exempt
def edit(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        post_id = data.get("id")
        content = data.get("content")
        post = Post.objects.get(pk=post_id)
        post.content = content
        post.save()
        return JsonResponse({
            "content": post.content
        })
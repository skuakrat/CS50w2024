import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import User, Post



def index(request):
    return render(request, "network/index.html", {
        "type": type,
    })
    

    
def profile(request, username):
    type = username
    user = get_object_or_404(User, username=username)

    if request.user.is_authenticated:
        followings_list = user.follows.values('username')
        followings_no = len(followings_list)
        followers_list = User.objects.filter(follows=user)
        followers_no = len(followers_list)

        usernames = [entry['username'] for entry in followings_list]
        fusernames = [entry.username for entry in followers_list]

        # Return JsonResponse with the necessary data
        return JsonResponse({
            "type": type,
            "profile": username,
            "followings_no": followings_no,
            "followers_no": followers_no,
            "followings_list": usernames,
            "followers_list": fusernames,
        })
    else:
        # Handle the case when the user is not authenticated (AnonymousUser)
        return JsonResponse({
            "type": type,
        })    



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
    


@csrf_exempt
@login_required
def compose(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)


    # Get contents of post
    data = json.loads(request.body)
    body = data.get("body", "")
    if not body:
        return JsonResponse({
            "error": "Post content required."
        }, status=400)

    # Create one email for each recipient, plus sender
    post = Post(
        user=request.user,
        body=body,
        )
    post.save()

    return JsonResponse({"message": "Post added successfully."}, status=201)



@csrf_exempt
@login_required
def edit(request, post_id):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)


    # Get contents of post    
    data = json.loads(request.body)
    body = data.get("body", "")
    if not body:
        return JsonResponse({
            "error": "Post content required."
        }, status=400)
    
    # Get current post
    post_id = data.get("post_id", "")
    post = Post.objects.get(pk=post_id)

    post.body = body
    post.save()

    return JsonResponse({"message": "Post edited successfully."}, status=201)





def load_post(request, type, page):
    

    if request.user.is_authenticated:

        
        if type == "follow":
            follows = request.user.follows.all()
            posts = Post.objects.filter(user__in=follows)

        elif type == "all":
            posts = Post.objects.all()
        
        else:
            user = get_object_or_404(User, username=type)
            posts = Post.objects.filter(
                user=user
            )
        
        posts = posts.order_by("-timestamp").all()
        paginator = Paginator(posts, 10) # Show 10 per page.
        page_number = page
        page_obj = paginator.get_page(page_number)
        return JsonResponse([post.serialize() for post in page_obj], safe=False)
    
    else:
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        posts = posts.order_by("-timestamp").all()
        paginator = Paginator(posts, 10) # Show 10 per page.
        page_number = page
        page_obj = paginator.get_page(page_number)
        return JsonResponse([post.serialize() for post in page_obj], safe=False)
    


def page(request, type, page):

    if request.user.is_authenticated:

        
        if type == "follow":
            follows = request.user.follows.all()
            posts = Post.objects.filter(user__in=follows)

        elif type == "all":
            posts = Post.objects.all()
        
        else:
            user = get_object_or_404(User, username=type)
            posts = Post.objects.filter(
                user=user
            )
        
        posts = posts.order_by("-timestamp").all()
        paginator = Paginator(posts, 10) # Show 10 per page.
        page_number = page
        page_obj = paginator.get_page(page_number)
        original_pagetotal = range(page_obj.paginator.num_pages)
        pagetotal = [i + 1 for i in original_pagetotal]
        return render(request, 'network/paginator.html', {
            'page_obj': page_obj,
            'type': type,
            'pagetotal': pagetotal
            })
    
    else:
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        paginator = Paginator(posts, 10) # Show 10 per page.
        page_number = page
        page_obj = paginator.get_page(page_number)
        original_pagetotal = range(page_obj.paginator.num_pages)
        pagetotal = [i + 1 for i in original_pagetotal]
        return render(request, 'network/paginator.html', {
            'page_obj': page_obj,
            'type': type,
            'pagetotal': pagetotal
            })



def follow(request, username):

    user = request.user
    profile = User.objects.get(username=username)

    if request.method == "GET":
        user.follows.add(profile)
        user.save()
        return JsonResponse({"message": "Successfully followed the user."})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=400)

def unfollow(request, username):

    user = request.user
    profile = User.objects.get(username=username)

    if request.method == "GET":     
        user.follows.remove(profile)
        user.save()
        return JsonResponse({"message": "Successfully unfollowed the user."})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=400)
    

def like(request, post_id):

    thispost = Post.objects.get(pk=post_id)
    user = request.user

    if request.method == "GET":
        thispost.likes.add(user)
        thispost.save()
        return JsonResponse({"message": "Successfully liked the post."})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=400)
    

def unlike(request, post_id):

    thispost = Post.objects.get(pk=post_id)
    user = request.user

    if request.method == "GET":
        thispost.likes.remove(user)
        thispost.save()
        return JsonResponse({"message": "Successfully unliked the post."})
    else:
        return JsonResponse({"message": "Invalid request method."}, status=400)

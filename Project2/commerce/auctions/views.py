from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal
from django.db.models import OuterRef, Subquery
from .models import User, Listing, Category, Bid, Comment






def index(request):
    listings = Listing.objects.filter(status=1).order_by('-id')
    latest_bidlist_subquery = Bid.objects.filter(bidlist=OuterRef('pk')).order_by('-id').values('bid')[:1]
    listings_with_latest_bidlist = listings.annotate(
        latest_bid=Subquery(latest_bidlist_subquery.values('bid')[:1])
    )


    return render(request, "auctions/index.html", {
        "listings": listings_with_latest_bidlist,
        "h2": "Active Listings"
    })

@login_required
def watchlist(request):
    user = request.user
    listings = Listing.objects.filter(watch=user).order_by('-id')
    
    return render(request, "auctions/index.html",{
        "listings": listings,
        "h2": "My watchlists",
    })

def categoryid(request, cat_id):
    listings = Listing.objects.filter(category_id=cat_id)
    category = Category.objects.get(pk=cat_id)
    latest_bidlist_subquery = Bid.objects.filter(bidlist=OuterRef('pk')).order_by('-id').values('bid')[:1]
    listings_with_latest_bidlist = listings.annotate(
    latest_bid=Subquery(latest_bidlist_subquery.values('bid')[:1])
    )
    return render(request, "auctions/index.html",{
        "listings": listings_with_latest_bidlist,
        "h2": f"{category}"
    })

def category(request):
    categorys = Category.objects.all()
    return render(request, "auctions/category.html",{
        "categorys": categorys
    })

@login_required
def listing(request,id):
    
    list = Listing.objects.get(pk=id)
    check_watch = list.watch.filter(id=request.user.id).exists()
    bidlists = Bid.objects.filter(bidlist=list).order_by('-id')
    comments = Comment.objects.filter(item=list)
    winbid = bidlists.first()

    if request.method == "POST":

        bid = Decimal(request.POST["bid"])
        if bid == winbid.bid:
            

            return render(request, "auctions/listing.html", {
            "message": "Not Successully. Note: *bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). Please try again.",  
            "danger": "danger",
            "list": list,
            "check_watch": check_watch,
            "bidlists": bidlists,
            "winbid": winbid,
            "comments": comments
            })
        else:
            Bid.objects.get_or_create(bidlist=list, bidder=request.user, bid=bid)
            return render(request, "auctions/listing.html", {
            "message": "Successully added your bid.",    
            "list": list,
            "check_watch": check_watch,
            "bidlists": bidlists,
            "winbid": winbid,
            "comments": comments
            })



    return render(request, "auctions/listing.html", {
        "list": list,
        "check_watch": check_watch,
        "bidlists": bidlists,
        "winbid": winbid,
        "comments": comments

    })



@login_required
def comment(request,id):
    if request.method == "POST":

        list = Listing.objects.get(pk=id)
        comment = request.POST["comment"]
        Comment.objects.get_or_create(item=list, owner=request.user, comment=comment)
        
        return render(request, "auctions/result.html",{
            "message": "Successully added the comment.",
            "id": id,
        })
        
    return HttpResponseRedirect(reverse("listing", args=[id]))

@login_required
def close(request,id):
    list = Listing.objects.get(pk=id)
    if request.method == "GET":
        list.status = 0
        list.save()
        return HttpResponseRedirect(reverse("listing", args=(id,)))

    return HttpResponseRedirect(reverse("listing", args=(id,)))


@login_required
def unwatch(request, id):
    list = Listing.objects.get(pk=id)
    list.watch.remove(request.user)

    return render(request, "auctions/result.html",{
        "message": "Successully removed from watchlist.",
        "id": id,
    })
    



@login_required
def watch(request,id):
    list = Listing.objects.get(pk=id)
    list.watch.add(request.user)

    return render(request, "auctions/result.html",{
        "message": "Successully added to watchlist.",
        "id": id,
    })
    




@login_required
def add(request):
    categorys = Category.objects.all()
    listings = Listing.objects.filter(status=1).order_by('-id')
    latest_bidlist_subquery = Bid.objects.filter(bidlist=OuterRef('pk')).order_by('-id').values('bid')[:1]
    listings_with_latest_bidlist = listings.annotate(
    latest_bid=Subquery(latest_bidlist_subquery.values('bid')[:1])
    )
    bidlists = Bid.objects.filter(bidlist__in=listings).order_by('-id')
    if request.method == "POST":
        owner = request.user
        title = request.POST["title"]
        description = request.POST["description"]
        url = request.POST["url"]
        category = Category.objects.get(pk=int(request.POST["category"]))
        firstbid = Decimal(request.POST["firstbid"])
        status = "1"
        addlisting = Listing.objects.create(owner=owner, title=title, description=description, url=url, 
                                            category=category, firstbid=firstbid, status=status)
        addlisting.save()
        addbid = Bid.objects.create(bidlist=addlisting, bidder=owner, bid=firstbid)
        addbid.save()


        return render(request, "auctions/index.html",{
            "message": "Successully added to active listing.",
            "listings": listings_with_latest_bidlist,
            "bidlists": bidlists
        })

    else:
        return render(request, "auctions/add.html", {
            "categorys": categorys
        })

        # return HttpResponseRedirect(reverse("flight", args=(flight.id,)))


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

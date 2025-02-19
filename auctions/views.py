from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Auction, User, Watchlist, Bid

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def index(request):
    auctions = Auction.objects.filter(is_closed = False)
    bids = Bid.objects.all()
    return render(request, "auctions/index.html", {
                  "auctions": auctions,
                  "bids": bids
    })


def login_view(request):
    if request.method == "POST":

        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        
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

        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        
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

def createList(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        url = request.POST["url"]
        starting_bid = request.POST["starting_bid"]
        user = request.user

        auction = Auction(title=title, description=description, image_url=url, user=user)
        auction.save()

        Bid.objects.create(auction=auction, user=user, value=starting_bid)

        return HttpResponseRedirect(reverse("Listing", kwargs={'id': auction.id}))
    else:
        return render(request, "auctions/createList.html")


def listing(request, id):
    auction = Auction.objects.get(pk = id)
    bids = auction.bids.order_by('-value')
    title = auction.title
    description = auction.description
    url = auction.image_url
    watchlist = Watchlist.objects.filter(auction = auction)
    auctions = Auction.objects.all()
    user = request.user
    current_bid = auction.bids.order_by('-value').first()

    return render(request, "auctions/listing.html", {
            "title": title,
            "description": description,
            "auction": auction,
            "auctions": auctions,
            "url":  url,
            "watchlist": watchlist,
            "bids": bids,
            "current_bid": current_bid,
            "user": user
        })

def watchlist(request):
    bids = Bid.objects.all()
    user = request.user
    watchlist = Watchlist.objects.filter(user = user)
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "user": user,
        "bids" : bids
    }) 

def removeWatchList(request):
    if request.method == "POST":
        title = request.POST["title"]
    user = request.user
    auction = Auction.objects.get(title = title)
    watchlist = Watchlist.objects.filter(user = user)
    watchlist.filter(auction = auction).delete()
    return HttpResponseRedirect(reverse("watchlist"))

def closeAuction(request):
    if request.method == "POST":
        auction_title = request.POST["title"]
        auction = get_object_or_404(Auction, title = auction_title)
        highest_bid = auction.bids.order_by('-value').first()

        if highest_bid:
            auction.winner = highest_bid.user
            auction.is_closed = True
            auction.save()

        return HttpResponseRedirect(reverse("index"))
    
def closeAuctionView(request):
    current_user = request.user
    closed_auctions = Auction.objects.filter(winner = current_user, is_closed = True)
    closed_auctions_exists = closed_auctions.exists()

    if closed_auctions_exists:
        return render(request, "auctions/closeAuctionView.html", {
                       "closed_auctions": closed_auctions
        })
    else:
        return render(request, "auctions/closeAuctionView.html", {
                       "message": "You have no closed auctions."
        })


def addWatchList(request):
    if request.method == "POST":
        title = request.POST["title"]

    user = request.user

    try:
        auction = Auction.objects.get(title = title)
    except Auction.DoesNotExist:
        return HttpResponse("Auction doesn't exist.")
    

    userWatchList = Watchlist.objects.filter(user = user) 

    if not userWatchList.filter(auction = auction).exists():
        watchlist = Watchlist.objects.create(user = user, auction = auction)
        watchlist.save()
        return HttpResponseRedirect(reverse("watchlist"))


def addListing(request):
    if request.method == "POST":
       user = request.user
       title = request.POST["title"]

       try:
           auction = Auction.objects.get(title = title)
       except Auction.DoesNotExist:
              return HttpResponse("Auction doesn't exist.")

       userWatchList = Watchlist.objects.filter(user = user)

       if not userWatchList.filter(auction = auction).exists():
           Watchlist.objects.create(user = user, auction = auction)
           return HttpResponseRedirect(reverse("watchlist"))
           
def submitBid(request):
    if request.method == "POST":
        auction_title = request.POST["title"]
        bid_value = float(request.POST["bid"])
        user = request.user

        auction = get_object_or_404(Auction, title=auction_title)
        highest_bid = auction.bids.order_by('-value').first()

        if highest_bid:
            if bid_value <= highest_bid.value:
                return render(request, 'auctions/error.html', {
                    'message': 'Bid must be higher than the current bid.'
                })
        else:
            if bid_value <= 0:
                return render(request, 'auctions/error.html', {
                    'message': 'Bid must be higher than 0.'
                })

        Bid.objects.create(auction=auction, user=user, value=bid_value)

        channel_layer = get_channel_layer()
        if channel_layer is None:
            raise ValueError("Channel layer is not configured!")
        async_to_sync(channel_layer.group_send)(
            f'auction_{auction.id}',
            {
                'type': 'auction_message',
                'message': {
                    'bid': bid_value,
                    'user': user.username
                }
            }
        )

        return redirect('Listing', id=auction.id)

    return HttpResponse("Invalid request method.")




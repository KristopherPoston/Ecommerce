from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createList", views.createList, name = "createList"),
    path("listing/<int:id>", views.listing, name = "Listing"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("addListing", views.addListing, name="addListing"),
    path("addWatchList", views.addWatchList, name="addWatchList"),
    path("removeWatchList", views.removeWatchList, name="removeWatchList"),
    path("closeAuction", views.closeAuction, name = "closeAuction"),
    path("closeAuctionView", views.closeAuctionView, name = "closeAuctionView"),
    path("submitBid", views.submitBid, name = "submitBid")
         
]

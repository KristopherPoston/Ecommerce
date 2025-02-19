from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    
    def __str__(self):
        return self.username

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.TextField()
    image_url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Creator", default=1)
    dateCreated = models.DateTimeField(default=timezone.now)
    is_closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="winner")

    def __str__(self):
        return self.title

    @property
    def current_price(self):
        highest_bid = self.bids.order_by('-value').first()
        return highest_bid.value if highest_bid else 0

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "poster")
    auction = models.ForeignKey(Auction, blank = True ,on_delete=models.CASCADE, related_name="watchlistEntry")
  
    def __str__(self):
        return f"{self.user.username} - {self.auction.title}"
    
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} bid {self.value} on {self.auction.title}"
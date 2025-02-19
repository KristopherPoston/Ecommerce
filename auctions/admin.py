from django.contrib import admin
from .models import Auction
from .models import Watchlist
from .models import User
from .models import Bid

# Register your models here.
admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(User)
admin.site.register(Bid)

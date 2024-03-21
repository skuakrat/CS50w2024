from django.contrib import admin
from .models import Category, Comment, Bid, Listing, User


class WatchlistAdmin(admin.ModelAdmin):
    filter_horizontal = ("user",)

class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ("watch",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("item","owner","comment",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("bidlist", "bidder", "bid",)


# Register your models here.

admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(User)


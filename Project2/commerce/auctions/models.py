from django.contrib.auth.models import AbstractUser
from django.db import models

class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category}"

class Comment(models.Model):
    item = models.ForeignKey("Listing", on_delete=models.CASCADE, related_name="commentitems")
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="commenters")
    comment = models.TextField()

    def __str__(self):
        return f"{self.owner} commented {self.comment}"

class Bid(models.Model):


    bidlist = models.ForeignKey("Listing", on_delete=models.CASCADE, blank=True, related_name="bidlists")
    bidder = models.ForeignKey("User", on_delete=models.CASCADE, related_name="bidders")
    bid = models.DecimalField(max_digits=16, decimal_places=2)

    def __str__(self):
        return f"{self.bidlist.title} {self.bidder} bidded {self.bid}"

class Listing(models.Model):
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="listers")
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=7000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    firstbid = models.DecimalField(max_digits=16, decimal_places=2)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="biddings", blank=True, null=True)
    status = models.IntegerField()
    watch = models.ManyToManyField("User", blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.title} by {self.owner}"



class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"
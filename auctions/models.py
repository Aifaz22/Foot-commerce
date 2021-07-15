from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.contrib.auth import get_user_model



class User(AbstractUser):
    Watchlist=models.ManyToManyField('Listing',blank=True)
    pass

class Categories(models.Model):
    category=models.CharField(max_length=150)
    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    Name = models.CharField(max_length=150)
    Description= models.CharField(blank=True, max_length=500)
    Price= models.DecimalField(decimal_places=2, max_digits=100)
    Image=models.CharField(blank=True, max_length=500)
    Owner= models.ForeignKey(User,on_delete=models.CASCADE)
    Category=models.ForeignKey(Categories,on_delete=models.CASCADE,default="No Category")
    PostDate=models.DateField(auto_now_add=True)
    PostTime=models.TimeField(auto_now_add=True)
    Bids=models.ManyToManyField('Bid',blank=True)
    Active=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.Name}"


class Bid(models.Model):
    Bidder=models.ForeignKey(User,on_delete=models.CASCADE)
    currentBid=models.PositiveIntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)
    class meta:
        ordering=['time']
    
    def __str__(self):
        return f"Current Bid: ${self.currentBid}"

class Comment(models.Model):
    Listing=models.ForeignKey(Listing,on_delete=models.CASCADE)
    content=models.CharField("",max_length=2000)
    date=models.DateTimeField(auto_now_add=True)
    User=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.User}: {self.content}"



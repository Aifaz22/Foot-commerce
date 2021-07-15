from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms

from .models import User, Listing, Bid, Comment, Categories
from django.db.models import Max

class ListingForm(ModelForm):
    if not Categories.objects.filter(category="No Category").exists():
        Categories(category="No Category").save()
    newCat= forms.CharField(label="", max_length=150, required=False, widget=forms.TextInput(attrs={"placeholder":"Other unlisted category" }))
    class Meta:
        model=Listing
        exclude = ['Owner', 'Bids','Active']
    

    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        #add class to each form fields for css
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

class newBid(forms.Form):
    newBid=forms.DecimalField(decimal_places=2, min_value=0)
    def __init__(self, *args, **kwargs):
        super(newBid, self).__init__(*args, **kwargs)
        #add class to each form fields for css
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })

class addComment(ModelForm):
    class Meta:
        model=Comment
        fields=['content']
        widgets={
            'content':forms.TextInput(attrs={'placeholder':'Add your comments here','size':70})
        }
    def __init__(self, *args, **kwargs):
        super(addComment, self).__init__(*args, **kwargs)
        #add class to each form fields for css
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
def index(request):
    return render(request, "auctions/index.html",{
        #get all active listings
        "listing":Listing.objects.filter(Active=True)
    })

def category(request):
    return render(request, "auctions/category.html",{
        #get all listed categories
        "cat":Categories.objects.all()
    })

def specificCat(request, cat):
    return render(request, "auctions/index.html",{
        "cat":cat,
        #get listings from specific cat
        "listing":Listing.objects.filter(Category__category=cat)
    })

# watchlist left
@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        #get listings from the watchlist
        "listing":request.user.Watchlist.all()
    })


@login_required
def createListing(request):
    form=ListingForm(request.POST)
    #check for form submission
    if request.method=="POST":
        if form.is_valid():
            Owner=request.user
            Name=form.cleaned_data['Name']
            Description=form.cleaned_data['Description']
            Price=form.cleaned_data['Price']
            newCat=form.cleaned_data['newCat']
            # add new category if needed or use the selected category
            # priority to new category***
            if len(newCat)>=1:
                if not Categories.objects.filter(category=newCat).exists():
                    Categories(category=newCat).save()
                Category=Categories.objects.get(category=newCat)
            else:
                Category=form.cleaned_data['Category']
            Image=form.cleaned_data['Image']
            if Image in [None,'']:
                Image="https://i.stack.imgur.com/y9DpT.jpg"
            bid=Bid(Bidder=Owner,currentBid=Price)
            bid.save()
            #create listing and save it in the database
            newListing=Listing(Owner=Owner,Name=Name,Description=Description,Price=Price,Category=Category,Image=Image)
            newListing.save()
            newListing.Bids.add(bid)
            newListing.save()
            return HttpResponseRedirect(reverse('listing',args={newListing.id})) # redirect to the new listing's page
    if not Categories.objects.filter(category="No Category").exists(): #check to make a "No Category" if its deleted
        Categories(category="No Category").save()
    return render(
        request, "auctions/createListing.html",{
            "form":ListingForm
        }
    )
# todo: comments section
def listing(request,ID):
    '''
        cases included:
            -form submission (post)
                -is logged in
                    -adding to watchlist
                    -removing from watchlist
                    -adding comment
                    -if it is the owner then option to end bidding
                    -if not the owner, add bids
                        -error: if the highest bidder bids again
                        -bid=starting bid
                        -bid>other bids
                        -error: when bid<=other bids
                - not logged in
                    -cant add/remove to/from watchlist, add bid or comments and end bidding
            - get request
                -is logged in
                    -can add/remove to/from watchlist, add bid or comments and end bidding
                -not logged in
                    -cant add/remove to/from watchlist, add bid or comments and end bidding
    '''
    listing=Listing.objects.get(pk=ID)
    maxBid=listing.Bids.latest('time')
    # check for form submission
    if (request.method=="POST"):
        if request.user.is_authenticated:
            #check if it is to add or remove from watchlist as update database accordingly
            if request.POST.get("modifier")=='Add to watchlist':
                request.user.Watchlist.add(listing)
                return render(
                            request,"auctions/listingPage.html",{
                                "listing":listing,
                                "bids":listing.Bids.all().count()-1,
                                "highestBid":listing.Bids.latest('time'),
                                "form":newBid,
                                "watching":listing in request.user.Watchlist.all(),
                                "loggedIn":request.user.is_authenticated,   
                                "isOwner":request.user==listing.Owner,
                                "commentForm":addComment,
                                "comments":Comment.objects.filter(Listing=listing)
                            }
                        )
            elif request.POST.get("modifier")=='Remove from watchlist':
                request.user.Watchlist.remove(listing)
                return render(
                            request,"auctions/listingPage.html",{
                                "listing":listing,
                                "bids":listing.Bids.all().count()-1,
                                "highestBid":listing.Bids.latest('time'),
                                "form":newBid,
                                "watching":listing in request.user.Watchlist.all(),
                                "loggedIn":request.user.is_authenticated,
                                "isOwner":request.user==listing.Owner,
                                "commentForm":addComment,
                                "comments":Comment.objects.filter(Listing=listing)
                            }
                        )
            # check if request is to post comment, if so add the comment
            if request.POST.get("comment")=='Post Comment':
                form=addComment(request.POST)
                if form.is_valid():
                    comment=form.cleaned_data['content']
                    newComment=Comment(Listing=listing,content=comment,User=request.user)
                    newComment.save()
                return render(
                        request,"auctions/listingPage.html",{
                            "listing":listing,
                            "bids":listing.Bids.all().count()-1,
                            "highestBid":listing.Bids.latest('time'),
                            "form":newBid,
                            "watching":listing in request.user.Watchlist.all(),
                            "loggedIn":request.user.is_authenticated,
                            "isOwner":request.user==listing.Owner,
                            "commentForm":addComment,
                            "comments":Comment.objects.filter(Listing=listing)
                        }
                    )
            # check if the request is mady by the owner, if so, confirm if it is to end the bidding and update database accordingly
            if request.user==listing.Owner:
                if request.POST.get('action')=='End Biddings':
                    listing.Active=False
                    listing.save()
                    return render(
                        request,"auctions/listingPage.html",{
                            "listing":listing,
                            "bids":listing.Bids.all().count()-1,
                            "highestBid":listing.Bids.latest('time'),
                            "form":newBid,
                            "watching":listing in request.user.Watchlist.all(),
                            "loggedIn":request.user.is_authenticated,
                            "isOwner":request.user==listing.Owner,
                            "commentForm":addComment,
                            "comments":Comment.objects.filter(Listing=listing)
                        }
                    )
            else:
                # This will have to be a request for adding a Bid as other cases checked previously and we check for different cases
                form=newBid(request.POST)
                if form.is_valid():
                    value=form.cleaned_data['newBid']
                    # max bidder bids again
                    ### show error==== !You are already the highest bidder!
                    if maxBid.Bidder==request.user:
                        return render(
                            request, "auctions/listingPage.html",{
                                "listing":listing,
                                "bids":listing.Bids.all().count()-1,
                                "form":newBid,
                                "error":"Error: You are already the highest bidder!",
                                "highestBid":listing.Bids.latest('time'),
                                "isOwner":request.user==listing.Owner,
                                "watching":listing in request.user.Watchlist.all(),
                                "loggedIn":request.user.is_authenticated,
                                "commentForm":addComment,
                                "comments":Comment.objects.filter(Listing=listing)
                            }
                        )
                    #correct starting bid made
                    if value==listing.Price and maxBid.Bidder==listing.Owner:
                        Listing.objects.filter(pk=ID).update(Price=value)
                        newBidMade=Bid(Bidder=request.user, currentBid=value)
                        newBidMade.save()
                        listing.Bids.add(newBidMade)
                        return render(
                            request, "auctions/listingPage.html",{
                                "listing":listing,
                                "bids":listing.Bids.all().count()-1,
                                "form":newBid,
                                "highestBid":listing.Bids.latest('time'),
                                "isOwner":request.user==listing.Owner,
                                "watching":listing in request.user.Watchlist.all(),
                                "loggedIn":request.user.is_authenticated,
                                "commentForm":addComment,
                                "comments":Comment.objects.filter(Listing=listing)
                            }
                        )
                    # correct bid made
                    elif value>listing.Price:
                        Listing.objects.filter(pk=ID).update(Price=value)
                        newBidMade=Bid(Bidder=request.user, currentBid=value)
                        newBidMade.save()
                        listing.Bids.add(newBidMade)
                        return render(
                            request, "auctions/listingPage.html",{
                                "listing":listing,
                                "bids":listing.Bids.all().count()-1,
                                "form":newBid,
                                "highestBid":listing.Bids.latest('time'),
                                "isOwner":request.user==listing.Owner,
                                "watching":listing in request.user.Watchlist.all(),
                                "loggedIn":request.user.is_authenticated,
                                "commentForm":addComment,
                                "comments":Comment.objects.filter(Listing=listing)
                            }
                        )
                    #incorrect bid made
                    ### show error==== !Bid should be greater than the price!
                    else:
                        return render(
                            request, "auctions/listingPage.html",{
                                "listing":listing,
                                "bids":listing.Bids.all().count()-1,
                                "form":newBid,
                                "error":"Error: Bid should be greater than the price",
                                "highestBid":listing.Bids.latest('time'),
                                "isOwner":request.user==listing.Owner,
                                "loggedIn":request.user.is_authenticated,
                                "watching":listing in request.user.Watchlist.all(),
                                "commentForm":addComment,
                                "comments":Comment.objects.filter(Listing=listing)
                            }
                        )   
        else:
            #user not logged in
            return render(
                request, "auctions/listingPage.html",{
                    "listing":listing,
                    "bids":listing.Bids.all().count()-1,
                    "highestBid":listing.Bids.latest('time'),
                    "loggedIn":request.user.is_authenticated,
                    "comments":Comment.objects.filter(Listing=listing)
                }
            )
    # for get requests (no form submissions)
    if request.user.is_authenticated:
        #display this for logged in user
        return render(
            request, "auctions/listingPage.html",{
                "listing":listing,
                "bids":listing.Bids.all().count()-1,
                "highestBid":listing.Bids.latest('time'),
                "form":newBid,
                "loggedIn":request.user.is_authenticated,
                "watching":listing in request.user.Watchlist.all(),
                "isOwner":request.user==listing.Owner,
                "commentForm":addComment,
                "comments":Comment.objects.filter(Listing=listing)
            }
        )
    else:
        #display this for a user logged out (no forms available)
        return render(
            request, "auctions/listingPage.html",{
                "listing":listing,
                "bids":listing.Bids.all().count()-1,
                "highestBid":listing.Bids.latest('time'),
                "form":newBid,
                "loggedIn":request.user.is_authenticated,
                "isOwner":request.user==listing.Owner,
                "commentForm":addComment,
                "comments":Comment.objects.filter(Listing=listing)
            }
        )
    

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

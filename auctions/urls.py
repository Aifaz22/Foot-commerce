from django.urls import path
from django.conf import settings

from . import views
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories",views.category, name="category"),
    path("categories/<str:cat>",views.specificCat, name="specificCat"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("createListing",views.createListing,name="createListing"),
    path("listing/<int:ID>",views.listing,name="listing")
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
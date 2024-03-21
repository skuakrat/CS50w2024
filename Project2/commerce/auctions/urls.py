from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("listing/<str:id>", views.listing, name="listing"),
    path("category", views.category, name="category"),
    path("category/<str:cat_id>", views.categoryid, name="categoryid"),
    path("watch/<str:id>", views.watch, name="watch"),
    path("unwatch/<str:id>", views.unwatch, name="unwatch"),
    path("watchlist", views.watchlist, name="watchlist"),

    path("close/<str:id>", views.close, name="close" ),
    path("comment/<str:id>", views.comment, name="comment" ),
]

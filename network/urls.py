
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("follow/<str:name>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("like", views.like, name="like"),
    path("edit", views.edit, name="edit")
]

from django.urls import path # type: ignore
from . import views

app_name = "soraguchi"

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("post_insert", views.post_insert, name="post_insert"),
    path("post_detail/<int:id>", views.post_detail, name="post_detail"),
    path("post_update/<int:id>", views.post_update, name="post_update"),
    path("post_delete/<int:id>", views.post_delete, name="post_delete"),
    path("register", views.register, name="register"),
    path("activate_user/<uuid:token>", views.activate_user, name="activate_user"),
    path("user_login", views.user_login, name="user_login"),
    path("user_logout", views.user_logout, name="user_logout"),
    path("user_detail/<int:id>", views.user_detail, name="user_detail"),
    path("user_update/<int:id>", views.user_update, name="user_update"),
    path("chat_view", views.chat_view, name="chat_view"),

]


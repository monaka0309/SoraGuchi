from django.urls import path # type: ignore
from . import views

app_name = "soraguchi"

urlpatterns = [
    path("", views.index, name="index"),
    path("post_insert", views.post_insert, name="post_insert"),
    path("post_detail/<int:id>", views.post_detail, name="post_detail"),
    path("post_update/<int:id>", views.post_update, name="post_update"),
    path("post_delete/<int:id>", views.post_delete, name="post_delete"),
    path("register", views.register, name="register"),
]

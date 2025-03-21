from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from .models import Posts
from . import forms

def index(request):
    posts = Posts.objects.order_by("-created_at").all()
    params = {
        "page_title": "投稿一覧",
        "posts": posts,
    }
    return render(request, "post/index.html", params)

def post_insert(request):
    insert_form = forms.PostModelForm(request.POST or None)
    if insert_form.is_valid():
        insert_form.save()
        return redirect("soraguchi:index")
    return render(request, "post/insert.html", context={
        "insert_form": insert_form,
    })

def post_detail(request, id):
    post = Posts.objects.get(pk=id)
    return render(request, "post/detail_post.html", context={
        "post": post
    })

def post_update(request, id):
    post = Posts.objects.get(pk=id)
    update_form = forms.PostUpdateModelForm(
        request.POST or None,
        instance=post
        )
    if update_form.is_valid():
        update_form.save()
        return redirect("soraguchi:index")
    return render(request, "post/update_post.html", context={
        "update_form": update_form,
        "id": post.id
    })

def post_delete(request, id):
    post = get_object_or_404(Posts, id=id)
    if request.method == "POST":
        post.delete()
        return redirect("soraguchi:index")
    return render(request, "post/index.html")

def register(request):
    regist_form = forms.RegistForm(request.POST or None)
    if regist_form.is_valid():
        regist_form.save(commit=True)
        return redirect("SoraGuchiApp:index")
    return render(request, "user/register.html", context={
        "regist_form": regist_form
    })
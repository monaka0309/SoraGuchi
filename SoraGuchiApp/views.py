from django.shortcuts import render # type: ignore
from django.shortcuts import redirect # type: ignore
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
    return render(request, "post/insert.html", context={
        "insert_form": insert_form
    })

# def post_update(request, id):
    


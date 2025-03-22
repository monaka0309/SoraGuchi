from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from .models import Posts, UserActivateToken
from . import forms
from django.contrib import messages # type: ignore
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore

def index(request):
    posts = Posts.objects.order_by("-created_at").all()
    params = {
        "page_title": "投稿一覧",
        "posts": posts,
    }
    return render(request, "post/index.html", params)

@login_required
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

@login_required
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

@login_required
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

def activate_user(request, token):
    activate_form = forms.UserActivateForm(request.POST or None)
    if activate_form.is_valid():
        # ユーザーの有効化
        UserActivateToken.objects.activate_user_by_token(token)
        messages.success(request, "ユーザーを有効化しました。")
    activate_form.initial["token"] = token
    return render(
        request, "user/activate_user.html", context={
            "activate_form": activate_form,
        }
    )

def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data["email"]
        password = login_form.cleaned_data["password"]
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get("next", "soraguchi:index")
            return redirect(next_url)
        else:
            messages.warning(request, "ログインに失敗しました")
    return render(
        request, "user/user_login.html", context={
            "login_form": login_form,
        }
    )

@login_required
def user_logout(request):
    logout(request)
    return redirect("soraguchi:index")


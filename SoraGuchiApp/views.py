from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.http import HttpResponseRedirect, Http404, JsonResponse  # type: ignore
from .models import User, Posts, UserActivateToken
from . import forms
from django.contrib import messages  # type: ignore
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash  # type: ignore
from django.contrib.auth.decorators import login_required  # type: ignore
from django.core.exceptions import PermissionDenied  # type: ignore
import boto3  # type: ignore
import json, os


def home(request):
    return render(request, "pages/home.html")


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
        post = insert_form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect("soraguchi:index")
    return render(request, "post/insert.html", context={
        "insert_form": insert_form,
    })


def post_detail(request, id):
    post = Posts.objects.get(pk=id)
    return render(request, "post/detail_post.html", context={
        "post": post,
        "user_id": request.user.id,
    })


@login_required
def post_update(request, id):
    post = Posts.objects.get(pk=id)
    update_form = forms.PostUpdateModelForm(
        request.POST or None,
        instance=post
    )
    if post.user.id != request.user.id:
        raise Http404
    if update_form.is_valid():
        update_form.save()
        return redirect("soraguchi:post_detail", post.id)
    return render(request, "post/update_post.html", context={
        "update_form": update_form,
        "id": post.id,
        "post": post,
    })


@login_required
def post_delete(request, id):
    post = get_object_or_404(Posts, id=id)
    if post.user.id != request.user.id:
        raise Http404
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


@login_required
def user_detail(request, id):
    user = User.objects.get(pk=id)
    if user != request.user:
        raise PermissionDenied  # ユーザーにアクセス権がない。
    return render(request, "user/user_detail.html", context={
        "user": user
    })


@login_required
def user_update(request, id):
    user = get_object_or_404(User, pk=id)
    if user != request.user:
        raise PermissionDenied  # ユーザーにアクセス権がない。
    user_update_form = forms.UserUpdateForm(
        request.POST or None,
        instance=user
    )

    if request.method == "POST":
        if user_update_form.is_valid():
            user_update_form.save()
            return redirect("soraguchi:user_detail", user.id)
    return render(request, "user/user_update.html", context={
        "user_update_form": user_update_form,
    })

# AIのモデルを指定されたモデルに質問を投げて、レスポンスをchat_viewメソッドに返す。
def generate_text(model_id, body):
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION'),
        )

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())
    return response_body

@login_required
def chat_view(request):
    model_id = 'amazon.titan-text-premier-v1:0'
    aiForm = forms.AiForm(request.POST or None)
    if aiForm.is_valid():
        prompt = aiForm.cleaned_data["content"]
    else:
        return render(request, "ai/chat_view.html", context={
            "aiForm": aiForm,
        })

    body = json.dumps({
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 3072,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 0.9
        }
    })

    # response_body = generate_text(model_id, body)

    # output_text = response_body['results'][0]['outputText'] if response_body['results'] else "結果なし"
    output_text = "申し訳ありません。ただいまメンテナンス中により、使用できません。"

    # コンソールで出力確認。
    # print(f"入力トークン: {response_body['inputTextTokenCount']}")
    # for result in response_body['results']:
    #     print(f"トークン数: {result['tokenCount']}")
    #     print(f"結果: {result['outputText']}")
    #     print(f"Completion reason: {result['completionReason']}")

    return render(request, "ai/result.html", context={
        "content": prompt,
        "output_text": output_text
        })





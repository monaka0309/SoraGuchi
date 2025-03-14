from django.shortcuts import render # type: ignore
from django.shortcuts import redirect # type: ignore
from django.http import HttpResponseRedirect # type: ignore
from .models import Posts
from .forms import PostForm

def index(request):
    # posts = Posts.objects.all()
    # params = {
    #     "page_title": "投稿一覧",
    #     "posts": posts,
    # }
    # return render(request, "index.html", params)
    return render(request, "index.html")

# def post_insert(request):
#     params = {
#         "page_title": "投稿入力フォーム",
#         "form": PostForm(),
#     }
#     if (request.method == "POST"):
#         title = request.POST["title"]
#         content = request.POST["content"]
#         post = Posts(title=title, content=content)
#         post.save()
#         return redirect(to="/soraguchi")
#     return render(request, "insert.html", params)




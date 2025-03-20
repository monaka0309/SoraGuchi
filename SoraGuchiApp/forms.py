from django import forms # type: ignore
from .models import Posts

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = "__all__"
        labels = {
            "title": "タイトル",
            "content": "内容",
        }

class PostUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "content"]


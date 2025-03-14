from django import forms # type: ignore

class PostForm(forms.Form):
    title = forms.CharField(label="タイトル")
    content = forms.CharField(label="内容")



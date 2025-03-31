from django import forms # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from django.contrib.auth.password_validation import validate_password # type: ignore
from django.core.exceptions import ValidationError # type: ignore
from .models import Posts

User = get_user_model()

class PostModelForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "content"]
        labels = {
            "title": "タイトル",
            "content": "内容",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"}),
            'content': forms.Textarea(attrs={'class': 'form-textarea w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]'}),
        }

class PostUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ["title", "content"]
        labels = {
            "title": "タイトル",
            "content": "内容",
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"}),
            'content': forms.Textarea(attrs={'class': 'form-textarea w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]'}),
        }

class RegistForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="パスワード再入力",
        widget = forms.PasswordInput(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"}),
    )
    class Meta():
        model = User
        fields = ("username", "email", "password")
        labels = {
            "username": "名前",
            "email": "メールアドレス",
            "password": "パスワード（8文字以上で数字、英字の大文字小文字を含んでください。）",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"}),
            'email': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]'}),
            'password': forms.PasswordInput(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"}),
        }
    
    # バリデーションチェック
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data["password"]
        confirm_password = cleaned_data["confirm_password"]
        if password != confirm_password:
            self.add_error("password", "パスワードが一致しません")
        try:
            validate_password(password, self.instance)
        except ValidationError as e:
            self.add_error("password", e)
        return cleaned_data
    
    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# トークンフォーム
class UserActivateForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"})
    )
    password = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"})
    )


class UserUpdateForm(forms.ModelForm):
    prefecture = forms.ChoiceField(
        choices=User.PREFECTURE_CHOICES,
        label="都道府県",
        widget=forms.Select(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"}),
        )
    class Meta:
        model = User
        fields = ["username", "email", "prefecture"]
        labels = {
            "username": "名前",
            "email": "メールアドレス",
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': "w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]"}),
            'email': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#00acc1]'}),
        }

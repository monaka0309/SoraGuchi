from django.db import models # type: ignore
from django.contrib.auth.models import ( # type: ignore
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Posts(BaseModel):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=140)
    class Meta:
        db_table = "posts"

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です")
        if not username:
            raise ValueError("ユーザー名は必須です")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields["is_staff"]=True
        extra_fields["is_active"]=True
        extra_fields["is_superuser"]=True
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionError):
    
    username = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    prefecure = models.CharField(max_length=50)
    picture = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email' # このテーブルのレコードを一意に識別するField
    REQUIRED_FIELDS = ['username'] # createsuperuserの時に入力を求められる
    class Meta:
        db_table = 'users'




from django.db import models # type: ignore
from django.contrib.auth.models import ( # type: ignore
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils import timezone # type: ignore
from datetime import timedelta
from uuid import uuid4
from django.dispatch import receiver # type: ignore
from django.db.models.signals import post_save # type: ignore


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
    picture = models.FileField(null=True, upload_to="picture/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email' # このテーブルのレコードを一意に識別するField
    REQUIRED_FIELDS = ['username'] # createsuperuserの時に入力を求められる
    class Meta:
        db_table = 'users'


class UserActivateTokenManager(models.Manager):
    
    # トークンを受け取ってユーザーを有効化する。
    def activate_user_by_token(self, token):
        user_activate_token = self.filter(
            token=token,
            expired_at__gte=timezone.now()
        ).first()
        if not user_activate_token:
            raise ValueError("トークンが存在しません")
        
        user = user_activate_token.user
        user.is_active = True
        user.save()
        return user
    
    # トークンを発行もしくは更新する。
    def create_or_update_token(self, user):
        token = str(uuid4())
        expired_at = timezone.now() + timedelta(days=1) # トークンの期限を1日にする
        user_token, created = self.update_or_create(
            user=user,
            defaults={"token": token, "expired_at": expired_at,}
        )
        return user_token

# UserActivateTokenテーブル情報
class UserActivateToken(models.Model):
    token = models.UUIDField(db_index=True, unique=True)
    expired_at = models.DateTimeField()
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE,
        related_name="user_activate_token",
    )
    
    objects: UserActivateTokenManager = UserActivateTokenManager()
    
    class Meta:
        db_table = "user_activate_token"

@receiver(post_save, sender=User)
def publish_token(sender, instance, created, **kwargs):
    user_activate_token = UserActivateToken.objects.create_or_update_token(instance)
    print(
        f"http://127.0.0.1:8000/soraguchi/activate_user/{user_activate_token.token}"
    )
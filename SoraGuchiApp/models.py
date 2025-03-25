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
    PREFECTURE_CHOICES = [
        ("", "都道府県を選んでください"),
        ("北海道", "北海道"),
        ("青森県", "青森県"),
        ("岩手県", "岩手県"),
        ("宮城県", "宮城県"),
        ("秋田県", "秋田県"),
        ("山形県", "山形県"),
        ("福島県", "福島県"),
        ("茨城県", "茨城県"),
        ("栃木県", "栃木県"),
        ("群馬県", "群馬県"),
        ("埼玉県", "埼玉県"),
        ("千葉県", "千葉県"),
        ("東京都", "東京都"),
        ("神奈川県", "神奈川県"),
        ("新潟県", "新潟県"),
        ("富山県", "富山県"),
        ("石川県", "石川県"),
        ("福井県", "福井県"),
        ("山梨県", "山梨県"),
        ("長野県", "長野県"),
        ("岐阜県", "岐阜県"),
        ("静岡県", "静岡県"),
        ("愛知県", "愛知県"),
        ("三重県", "三重県"),
        ("滋賀県", "滋賀県"),
        ("京都府", "京都府"),
        ("大阪府", "大阪府"),
        ("兵庫県", "兵庫県"),
        ("奈良県", "奈良県"),
        ("和歌山県", "和歌山県"),
        ("鳥取県", "鳥取県"),
        ("島根県", "島根県"),
        ("岡山県", "岡山県"),
        ("広島県", "広島県"),
        ("山口県", "山口県"),
        ("徳島県", "徳島県"),
        ("香川県", "香川県"),
        ("愛媛県", "愛媛県"),
        ("高知県", "高知県"),
        ("福岡県", "福岡県"),
        ("佐賀県", "佐賀県"),
        ("長崎県", "長崎県"),
        ("熊本県", "熊本県"),
        ("大分県", "大分県"),
        ("宮崎県", "宮崎県"),
        ("鹿児島県", "鹿児島県"),
        ("沖縄県", "沖縄県"),
        ("その他", "その他"),
    ]

    username = models.CharField(max_length=15)
    email = models.EmailField(max_length=255, unique=True)
    # ユーザー登録時のメール確認を追加する際にFalseに変更予定。
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    prefecture = models.CharField(max_length=10, choices=PREFECTURE_CHOICES, null=True)
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
    # 登録後にメールで確認リンクを送信し、ユーザーがクリックすると is_active=True にする仕組みが作れる。
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

class Posts(BaseModel):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=140)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    class Meta:
        db_table = "posts"
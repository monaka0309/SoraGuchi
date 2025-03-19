from django.db import models # type: ignore


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


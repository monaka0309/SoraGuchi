from django.db import models # type: ignore

class Posts(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=140)
    class Meta:
        db_table = "posts"


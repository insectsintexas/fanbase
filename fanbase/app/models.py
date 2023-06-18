from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    body = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)

    is_private = models.BooleanField(default=False)  # ログインが必要な記事かどうかのフラグ
    author = models.ForeignKey(User, on_delete=models.CASCADE)

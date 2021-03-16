from django.db import models
from django.urls import reverse
from django.conf import settings
from registration.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        unique=True)
    
    def __str__(self):
        return self.name



class Post(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="作成日"
    )
    
    updated = models.DateTimeField(
        auto_now=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="最終更新日"
    )
        
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="タイトル"
    )
        
    body = models.TextField(
        blank=True,
        null=False,
        verbose_name="本文"
    )
     #ひとつの投稿にひとつしか付けれないからForeignKey
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="カテゴリー"
    )
     #ひとつの投稿に複数付けれるからManyToManyField
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="タグ"
    )
        
    published = models.BooleanField(
        default=True,
        verbose_name="公開する"
    )
     #ForeignKeyの引数は紐付けたいモデル項目(今回はユーザーIDを持たせたいからregistration/models/User)
    accessuser = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
     # いいねボタン  #ひとつの投稿のいいねに複数のユーザーのいいね付けれるようManyToManyField
    like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="post_like"
    )

     #投稿ボタン押した先に移行するhtmlの設定
    def get_absolute_url(self):
        return reverse("blog:index")

     #いいね情報を記録するページの設定
    def get_api_like_url(self):
        return reverse("blog:like_api", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Comment(models.Model):

     #記事に紐づくコメント
    text = models.TextField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="コメント内容"
    )

    target = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="対象記事"
    )

    def __str__(self):
        return self.text[:20]
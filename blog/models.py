from django.db import models
from django.urls import reverse_lazy
from django.urls import reverse
from django.conf import settings

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
        verbose_name="本文",
        help_text="HTMLタグは使えません。"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="カテゴリ"
    )
        
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        verbose_name="タグ"
    )
        
    published = models.BooleanField(
        default=True,
        verbose_name="公開する"
    )
      # いいね情報
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_like')

     #いいねを設置するページのURLを取得する設定
    def get_absolute_url(self):
        return reverse('blog:index')

     #いいね情報を記録するページの設定
    def get_api_like_url(self):
        return reverse('blog:like_api', kwargs={"pk": self.pk})

    def __str__(self):
        return self.titles
        
        
      #いいねボタン実装    
class LikeButtonModel(models.Model):
      # ユーザー情報
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    title    = models.CharField(max_length=100)
    slug     = models.SlugField()
    body     = models.TextField()
    date     = models.DateTimeField(auto_now_add=True)
    thumb    = models.ImageField(default='default.png', blank=True)
      # いいね情報
    like     = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')

     #いいねを設置するページのURLを取得する設定
    def get_absolute_url(self):
        return reverse('blog:index', kwargs={"slug": self.slug})

     #いいね情報を記録するページの設定
    def get_api_like_url(self):
        return reverse('blog:like_api', kwargs={"slug": self.slug})

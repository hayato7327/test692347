from django.contrib import admin
from django import forms
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class PostInline(admin.TabularInline):
    model = models.Post
    fields = ("title", "body","tags")
    extra = 1


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline]


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    pass


class PostAdminForm(forms.ModelForm):
    class Meta:
        labels = {
            "title": "ブログタイトル"
        }
        

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created", "updated")
     #fieldsetsに指定すれば管理画面の項目に追加できる
    fieldsets = [
        (None, {"fields": ("title", )}),
        ("本文", {"fields": ("body", )}),
        ("カテゴリー タグ", {"fields": ("category", "tags")}),
        ("日付", {"fields": ("created", "updated")}),
        ("いいね", {"fields": ("like",)}),
        ("投稿者", {"fields": ("accessuser",)}),
    ]

    form = PostAdminForm
    filter_horizontal = ("tags",)
        
    
    list_display = ("id", "title", "category", "tags_summary", "accessuser", "created", "updated")
    list_select_related = ("category", ) # N+1問題を解消
    list_editable = ("title", "category")
    search_fields = ("title", "category__name", "tags__name", "body", "created", "updated")
    ordering = ("-updated", "-created")
    list_filter = ("category", "tags", "created", "updated")
    
    def tags_summary(self, obj):
        qs = obj.tags.all()
        label = ', '.join(map(str, qs))
        return label
        
    tags_summary.short_description = "タグ"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("tags") # N+1問題を解消


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(get_user_model())
class UserAdmin(UserAdmin):

    fieldsets = [
        (None, {"fields": ("username", )}),
        ("メールアドレス", {"fields": ("email", )}),
    ]
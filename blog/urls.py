from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin
from .views import LikeButton


app_name = "blog" #アプリが複数ある時は、どのアプリのurlを指定してるかわかるようにapp_nameを指定する
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("mypage", views.Mypage.as_view(), name="mypage"),
    path("change_data", views.change_data, name="change_data"),
    path("comment_create/<int:pk>/", views.CommentCreate.as_view(), name="comment_create"),
    path("detail/<int:pk>/", views.Detail.as_view(), name="detail"),
    path("detail_user/<int:pk>/", views.DetailUser.as_view(), name="detail_user"),
    path('create/', views.Create.as_view(), name="create"),
    path("update/<int:pk>/", views.Update.as_view(), name="update"),
    path("comment_update/<int:pk>/", views.CommentUpdate.as_view(), name="comment_update"),
    path("delete/<int:pk>/", views.Delete.as_view(), name="delete"),
    path("comment_delete/<int:pk>/", views.CommentDelete.as_view(), name="comment_delete"),
     #いいね情報を格納するページ
    path("like/<int:pk>/", LikeButton.as_view(), name="like_api"),
]
from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin
from .views import LikeButton


app_name = "blog" #アプリが複数ある時は、どのアプリのurlを指定してるかわかるようにapp_nameを指定する
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("mypage", views.Mypage.as_view(), name="mypage"),
    path("search/", views.Search.as_view(), name="search"),
    path("search_category/", views.SearchCategory.as_view(), name="search_category"),
    path("search_tag/", views.SearchTag.as_view(), name="search_tag"),
    path("detail/<int:pk>/", views.Detail.as_view(), name="detail"),
    path('create/', views.Create.as_view(), name="create"),
    path("update/<int:pk>/", views.Update.as_view(), name="update"),
    path("delete/<int:pk>/", views.Delete.as_view(), name="delete"),
     #いいね情報を格納するページ
    path("like/<int:pk>/", LikeButton.as_view(), name="like_api"),
]

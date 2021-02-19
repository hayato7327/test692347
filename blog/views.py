from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import LikeButtonModel


# ListViewとDetailViewを取り込み
from django.views.generic import ListView, DetailView

# 自分で作ったPostモデルを取り込み
from .models import Post

# 一覧
class Index(ListView):
    # 一覧するモデルを指定 -> `object_list`で取得可能
    model = Post

# 個別
class Detail(DetailView):
    # 詳細表示するモデルを指定 -> `object`で取得可能
    model = Post
    

from django.views.generic.edit import CreateView

class Create(CreateView):
    model = Post
    
    # 編集対象にするフィールド
    fields = ["title", "body", "category", "tags"]
    

from django.views.generic.edit import UpdateView

class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags"]
    
    
from django.views.generic.edit import DeleteView

class Delete(DeleteView):
    model = Post
    
    # 削除したあとに移動する先（トップページ）
    success_url = "/"
    
    
    
class LikeButton(APIView):
    authentication_classes = (authentication.SessionAuthentication,) #ユーザーが認証されているか確認
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Post, pk=pk) #いいねボタンを設置しているページの情報取得
        url_ = obj.get_absolute_url() #いいねボタンを設置しているページのURL取得
        status = request.GET.getlist('status') #後半戦で説明
        status = bool(int(status[0])) 
        user = self.request.user #ユーザー情報の取得
        if user in obj.like.all(): #ユーザーがいいねをしていた場合
            if not(status):
                liked = True
            else:
                obj.like.remove(user) #likeからユーザーを外す
                liked = False
        else: #ユーザーがいいねをしていない場合
            if not(status):
                liked = False
            else:
                obj.like.add(user) #likeにユーザーを加える
                liked = True
        data = {
            "liked": liked,
        }
        return Response(data)

    
    

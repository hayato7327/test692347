from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post


class Index(ListView):
    model = Post


class Detail(DetailView):
    model = Post
    def get_template_names(self):
        if self.object.accessuser == self.request.user:
            template_name = 'post_detail.html'
        else:
            template_name = 'blog/invalid.html'
        return template_name
    

class Create(CreateView):
    model = Post
    fields = ["title", "body", "category", "tags"]


class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags"]
    

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

    
    

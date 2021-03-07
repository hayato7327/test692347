from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Category, Tag
from django.db.models import Q


class Index(ListView):
    model = Post
    context_object_name = 'post_list'
    queryset = Post.objects.order_by('category')
    model = Post
    paginate_by = 7

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['category_list'] = Category.objects.all()
        return context


class Search(ListView):
    model = Post

    def get_queryset(self): #検索関数  queryは設置html、post_list.htmlで定義
        q_word = self.request.GET.get("query")
        if q_word:
            object_list = Post.objects.filter(
                Q(title__icontains=q_word) |  #icontains = 部分一致
                Q(body__icontains=q_word))
        else:
            object_list = Post.objects.all() #もしフォームに何も入力せずに検索ボタン押したら、何も起こらない(ボタン押下前同様、投稿全表示)
        return object_list


class SearchCategory(ListView):
    model = Post
    

    def get_queryset(self): #検索関数  queryは設置html、post_list.htmlで定義
        q_word = self.request.GET.get("query_cate")
        print("q_word")
        print(q_word)
        if q_word:
            object_list = Post.objects.filter(
                Q(category__icontains=q_word)) #icontains = 部分一致
        else:
            object_list = Post.objects.all() #もしフォームに何も入力せずに検索ボタン押したら、何も起こらない(ボタン押下前同様、投稿全表示)
        return object_list


class Detail(DetailView):
    model = Post                                             
                                                             
     #ユーザーIDにより処理を変化
    def get_template_names(self): #get_template_names関数は動的にtemplate_nameを指定できる
        if self.object.accessuser == self.request.user: #もし、Detail.objectのaccessuser(modelsで定義)が、Detailにログインしてるユーザーと一致したら
            template_name = "blog/post_detail.html" #編集削除ができる通常の移行先、post_detail.htmlを表示させる
        else:
            template_name = "blog/other_user_detail.html" #違ったら、編集削除ができないhtml(other_user_detail.html)を表示
        return template_name
    

class Create(CreateView):
    model = Post
    fields = ["title", "body", "category", "tags"]
                                                            
    def form_valid(self, form): #form_validはフォームバリデーションに問題がなかった時に行う処理を記述する関数
        post = form.save(commit=False) #入力フォームを仮セーブし
        post.accessuser = self.request.user #そのフォームをPOSTしてきたユーザをaccessuserに入れて、accessuserとログインユーザーが一緒だったら
        post.save() # データベースに本セーブする
        return super().form_valid(form) #returnでform_validを親クラスのCreateに返す。親クラスに返すときはsuper()が必要


class Update(UpdateView):
    model = Post
    fields = ["title", "body", "category", "tags"]

     #もし投稿者じゃないユーザーがURLを直接指定してきて、投稿者じゃないのに編集画面に入ろうとしたら、悪意あるユーザーと判断し「無効なリンクです」と表示させる
    def get_template_names(self):
        if self.object.accessuser == self.request.user:
            template_name = "blog/post_form.html"

        else:
            template_name = "blog/invalid.html"
        return template_name
    

class Delete(DeleteView):
    model = Post

     #もし投稿者じゃないユーザーがURLを直接指定してきて、投稿者じゃないのに削除画面に入ろうとしたら、悪意あるユーザーと判断し「無効なリンクです」と表示させる
    def get_template_names(self):
        if self.object.accessuser == self.request.user:
            template_name = "blog/post_confirm_delete.html"

        else:
            template_name = "blog/invalid.html"
        return template_name
    
    # 削除したあとに移動する先（トップページ）
    success_url = "/"
    
    
    
class LikeButton(APIView):
    authentication_classes = (authentication.SessionAuthentication,) #ユーザーが認証されているか確認
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None, format=None):
        obj = get_object_or_404(Post, pk=pk) #いいねボタンを設置しているページの情報取得
        url_ = obj.get_absolute_url() #いいねボタンを設置しているページのURL取得
        status = request.GET.getlist("status")
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
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Category, Tag, Comment
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from blog.forms import UserChangeForm, CommentCreateForm
import time
from django.db.models import Count


@login_required
def change_data(request):
 
    form = UserChangeForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("blog:index")
 
    context = {
        "form": form,
    }
    return render(request, "blog/change_data.html", context)



       #トップページ
class Index(ListView):
    model = Post
    paginate_by = 5
    
    #検索関数
    def get_queryset(self):
        posts = Post.objects.all() # ここで１度全てのPOSTオブジェクトを取得します。
        
        q_word = self.request.GET.get("query")
        if q_word:
            posts = posts.filter(
                Q(title__icontains=q_word) |  # Q = titleもしくはbodyで検索という意味 title単体検索の場合いらない
                Q(body__icontains=q_word)     #icontains = フォームに入力した検索ワードにbodyに書かれてる文字列が部分一致したら
                )
            return posts

        elif "query_cate" in self.request.GET:
            return posts.filter(category__id=self.request.GET.get("query_cate"))

        elif "query_tag" in self.request.GET:
            return posts.filter(tags__id=self.request.GET.get("query_tag"))

        elif "query_like" in self.request.GET:
            if self.request.GET["query_like"] == "1":
                return posts.annotate(like_count=Count("like")).order_by("-like_count")
            else:
                return posts.annotate(like_count=Count("like")).order_by("like_count")
        else:
            return posts.order_by("-created") #URLが上記以外(トップページ)の時は投稿を新しい順に全て表示

    #プルダウンに項目を渡す関数
    def get_context_data(self, *args, **kwargs):
        time.sleep(1)
        context = super().get_context_data(*args, **kwargs)
        context["category_list"] = Category.objects.all() #トップページIndexのプルダウンに、存在する全てのカテゴリーを渡す
        context["selected_category"] = int(self.request.GET.get("query_cate", 0)) #カテゴリー検索したら、その選択したカテゴリーがなんだったのかselected_categoryに入れる
                                                                               #GETで取得した値は文字列なので、intで数値に変換する
        context["tags_list"] = Tag.objects.all()
        context["selected_tag"] = int(self.request.GET.get("query_tag", 0)) #self.request.GET.getが空の時は仮の値0を渡さないと、int() argument must be a string, a bytes-like object or a number, not 'NoneType' エラーになる
        context["like_list"] = [{"id": 1, "name": "いいね多い順"}, {"id": 2, "name": "いいね少ない順"}]
        context["selected_like"] = int(self.request.GET.get("query_like", 0))
        return context


class Mypage(ListView):
    model = Post
    template_name = "blog/mypage.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # 自分の記事をmy_postsに入れてhtmlで使えるようにする
        context["my_posts"] = Post.objects.filter(accessuser_id=self.request.user)
        # いいねした記事をlike_postsに入れてhtmlで使えるようにする
        context["like_posts"] = Post.objects.filter(like=self.request.user)
        return context


class Detail(DetailView):
    model = Post                                             
                                                             
     #ユーザーIDにより処理を変化
    def get_template_names(self): #get_template_names関数は動的にtemplate_nameを指定できる
        if self.object.accessuser == self.request.user: #もし、Detail.objectのaccessuser(modelsで定義)が、Detailにログインしてるユーザーと一致したら
            template_name = "blog/post_detail.html" #編集削除ができる通常の移行先、post_detail.htmlを表示させる
        else:
            template_name = "blog/other_user_detail.html" #違ったら、編集削除ができないhtml(other_user_detail.html)を表示
        return template_name


class CommentCreate(CreateView):

     #記事へのコメント作成ビュー
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs["pk"]
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.target = post
        comment.accessuser = self.request.user
        comment.save()
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs["pk"])
        return context


class Create(CreateView):
    model = Post
    fields = ["title", "body", "category", "tags"]
                                                            
    def form_valid(self, form): #form_validはフォームバリデーションに問題がなかった時に行う処理を記述する関数。今回は投稿にユーザーIDを持たせる
        post = form.save(commit=False) #入力フォームを仮セーブし
        post.accessuser = self.request.user #そのフォームをPOSTしてきたユーザをmodelsのaccessuserに入れて、accessuserとログインユーザーが一緒だったら
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


class CommentUpdate(UpdateView):
    model = Comment
    form_class = CommentCreateForm

    def get_template_names(self):
        if self.object.accessuser == self.request.user:
            template_name = "blog/comment_form.html"
        else:
            template_name = "blog/invalid.html"

        return template_name

         #class CommentUpdateを実行する直前のコメント内容のデータをpostに保存する
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.object.target
        return context
    

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


class CommentDelete(DeleteView):
    model = Comment

    def get_template_names(self):
        if self.object.accessuser == self.request.user:
            template_name = "blog/comment_delete.html"
        else:
            template_name = "blog/invalid.html"
        return template_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = self.object.target
        return context

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
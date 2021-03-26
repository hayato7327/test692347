# Python/Djangoでブログアプリを作成しました

## 目次

1.アプリの概要  
2.作ろうと思った理由  
3.使用した技術  
4.実装した機能  
5.工夫した点  
6.苦労したこと  
7.常に意識したこと  

### 1.アプリの概要

このアプリは、現在ぼっちで寂しい思いをしてる人達が最近あった悲しい出来事などをブログ形式で投稿し、それを会員同士で共有できるコミュニティです。  
ユーザー同士で投稿されたブログに対して「いいね」を付けあったりできるので、人気の記事がわかりやすいです。また、高評価を得るよう投稿内容のクオリティやモチベーションを高められます。  
また、検索機能もあるので見たいブログを素早く見つけられます。  

### 2.作ろうと思った理由

社会問題になりつつある「ぼっち」 この寂しさは経験者にしかわかりません。そこで、ぼっち経験者のみが集まるコミュニティを作って仲間同士で盛り上がれるコミュニティがあると良いなと思ったので作ってみました。  

### 3.使用した技術

インフラにheroku  
データベースにSQLite3  
使用言語にPython  
フレームワークにDjango   
フロントエンド言語にHTML CSS Javascript jquery/Ajax  
メールサーバーにmailgun  

### 4.実装した機能

新規会員登録、ログイン、ログアウト、パスワード変更、会員情報変更  
CRUD機能   
投稿検索機能  
いいねボタン  
無限スクロール  

### 5.工夫した点

1.  タップ操作をなるべく減らしてユーザビリティを向上させたいと思い、ページネーションではなく無限スクロールを実装  

`blog/post_list.html`118行目

```py
{% block extrajs %}
<script>
var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
    $('.loading').show();
    },
    onAfterPageLoad: function () {
    $('.loading').hide();
    }
});
</script>
{% endblock %}
```
  
2.  ユーザーの閲覧、評価をわかりやすく可視化したいと思い、いいねボタンを実装

`static/like.js`

```py
$(".like-btn").click(function(e){
  e.preventDefault()
  const this_ = $(this);
  const data_id = this_.attr("data-id")
  const like_cnt = $("#like"+data_id);
  const likeUrl = this_.attr("data-href");
  if (likeUrl){
    $.ajax({
      url: likeUrl,
      method: "GET",
      data: {"status":1}, //　いいねが押されましたと伝える
    })
    .then(
      function(data){
        let change_like = Number(like_cnt.text());
        if (data.liked){　//　もしいいねされていなかったら
          like_cnt.text(++change_like);　//　いいねの数を１追加
          this_.addClass("on");　//　ボタンをピンクに
        } else {　　//　もしいいねされていたら
          like_cnt.text(--change_like);　//　いいねの数を１減らす
          this_.removeClass("on");　//　ボタンのデザインを初期状態に
        }
      },
```

`blog/post_list.html`93行目

```py
<button class="like-btn {% if request.user in post.like.all %}on{% endif %}"
                       data-href="{{ post.get_api_like_url }}" data-id="{{post.pk}}">
          <span class="liked-cnt" id="like{{post.pk}}">{{ post.like.count }}</span>
          <i class="fas fa-thumbs-up"></i>
    </button>
```
  
3. 管理画面のブログ一覧画面Postsを開いた時、読み込みが遅かったのでなぜかと思ったらN+1問題が発生していた。

`blog/admin.py`48行目

```py
list_display = ("id", "title", "category", "tags_summary", "published", "created", "updated")
```
ブログが100件あると仮定する。ここでcategoryを取得する時、Post一覧取得にDBアクセス1回+100回DBアクセスが入ってしまい、読み込みが遅くなっていた。

  

```py
list_display = ("id", "title", "category", "tags_summary", "published", "created", "updated")
list_select_related = ("category", )
```
↑ list_select_related関数でcategoryを指定することにより、N+1問題を解消  

tag取得時も同様なので、prefetch_relatedでtagをあらかじめ事前ロードすることにより、N+1問題を解消
```py
def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("tags")
```



4. 投稿編集フォームページはそのブログの投稿者以外が入れたらまずいので、URLを直接指定してくる悪意あるユーザー対策としてセキュリティを強化

`blog/views.py`133行目

```py
#もし投稿者じゃないユーザーがURLを直接指定してきて、投稿者じゃないのに編集画面に入ろうとしたら、悪意あるユーザーと判断し「無効なリンクです」と表示させる
    def get_template_names(self):
        if self.object.accessuser == self.request.user:
            template_name = "blog/post_form.html"

        else:
            template_name = "blog/invalid.html"
        return template_name
```



5. テストコードを書いて動作に問題ないかを確認

`blog/tests/test_models.py`

```py
     #初期状態では何も登録されていないかテスト    
    def test_is_empty(self):
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)
        
        
         #レコードを１つ作成するとレコードが１つだけカウントされるかテスト
    def test_is_count_one(self):
        category = Category(name="テストカテゴリー")
        category.save()
        tag = Tag(name="テストタグ")
        tag.save()
        post = Post(category=category,title="test_title",
                    body="test_body", published=1)
        post.save()
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 1)
        
        
         #内容を指定してデータを保存し、すぐに取り出した時に
         #保存した時と同じ値が返されることをテスト
    def test_saving_retrieving_post(self):
        category = Category(name="テストカテゴリー")
        category.save()
        tag = Tag(name="テストタグ")
        tag.save()
        post = Post(category=category,title="test_title",
                    body="test_body", published=1)
        post.save()
        
        saved_posts = Post.objects.all()
        actual_post = saved_posts[0] #0は、saved_postsというリストから最初の値を取り出すという意味。2番目の値を取り出すなら1
        
        self.assertEqual(actual_post.title, "test_title")
        self.assertEqual(actual_post.body, "test_body")
        self.assertEqual(actual_post.published, 1)
```

`blog/tests/test_urls.py`

```py
     #トップページ/8000に移行するかテスト
         #blog/post_list.htmlを表示するかテスト
    def test_index_url(self):
        user = User.objects.create_user(username = "nomura100",password = "adgjm135")
        self.client.force_login(user)
        url = reverse("blog:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200) #200はdjangoで決められた正常値であったときに返される数値
        template = "blog:post_list.html"
        self.assertTemplateUsed(template)
       
        
         #/detail/<pk>/に移行するかテスト
         #blog/post_detail.htmlを表示するかテスト
    def test_detail_url(self):
        category = Category(name="テストカテゴリー")
        category.save()
        tag = Tag(name="テストタグ")
        tag.save()
        post = Post(category=category,title="test_title",
                    body="test_body", published=1)
        post.save()
        
        url = reverse("blog:detail", kwargs={"pk": post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        template = "blog/post_detail.html"
        self.assertTemplateUsed(template)
        
        
         #/create/に移行するかテスト
         #blog/post_form.htmlを表示するかテスト
    def test_create_url(self):
        url = reverse("blog:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        template = "blog:post_form.html"
        self.assertTemplateUsed(template)
        
        
         #/update/<pk>/に移行するかテスト
         #blog/post_form.htmlを表示するかテスト
    def test_update_url(self):
        category = Category(name="テストカテゴリー")
        category.save()
        tag = Tag(name="テストタグ")
        tag.save()
        post = Post(category=category,title="test_title",
                    body="test_body", published=1)
        post.save()
        
        url = reverse("blog:update", kwargs={"pk": post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        template = "blog:post_form.html"
        self.assertTemplateUsed(template)
        
        
         #/delete/<pk>/に移行するかテスト
         #blog/post_comfirm_delete.htmlを表示するかテスト
    def test_delete_url(self):
        category = Category(name="テストカテゴリー")
        category.save()
        tag = Tag(name="テストタグ")
        tag.save()
        post = Post(category=category,title="test_title",
                    body="test_body", published=1)
        post.save()
        
        url = reverse("blog:delete", kwargs={"pk": post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        template = "blog/post_comfirm_delete.html"
        self.assertTemplateUsed(template)
```

`blog/tests/views.py`

```py
       #ログイン時、ユーザー名nomura100が含まれているか確認 
class Test_Login(TestCase):
    
    def test_authenticated(self):
        user = User.objects.create_user(username = "nomura100",password = "adgjm135")
        self.client.force_login(user)
        url = reverse("blog:index")
        response = self.client.get(url)
        self.assertEqual(user.username, "nomura100")
```



6.  ユーザーが探したいブログをすぐ探せたらいいなと思い、さまざまなタイプの検索フォームを実装

`blog/views.py`39行目

get_querysetを使い、ブログの「タイトル、本文」からワード検索
```py
def get_queryset(self):
        posts = Post.objects.all() # ここで１度全てのPOSTオブジェクトを取得します。
        
        q_word = self.request.GET.get("query")
        if q_word:
            posts = posts.filter(
                Q(title__icontains=q_word) |  # Q = titleもしくはbodyで検索という意味 title単体検索の場合いらない
                Q(body__icontains=q_word)     #icontains = フォームに入力した検索ワードにbodyに書かれてる文字列が部分一致したら
                )
            return posts
```

カテゴリーで検索も可能
```py
elif "query_cate" in self.request.GET:
            return posts.filter(category__id=self.request.GET.get("query_cate"))
```

付いてるタグでも検索可能
```py
elif "query_tag" in self.request.GET:
            return posts.filter(tags__id=self.request.GET.get("query_tag"))
```

いいね順でも検索可能
```py
elif "query_like" in self.request.GET:
            if self.request.GET["query_like"] == "1":
                return posts.annotate(like_count=Count("like")).order_by("-like_count")
            else:
                return posts.annotate(like_count=Count("like")).order_by("like_count")
```



7. 会員登録の認証リンクをクリックしたら、自動でログイン化し、ユーザーの負担を軽減

`registration/forms.py`74行目

```py
login(request, user, backend='django.contrib.auth.backends.ModelBackend')
```



8. 無限スクロールで一番下に行って、もし一番上に戻りたいと思った時一発で戻れるよう、トップページリンクであるへーダーをスクロール時も常時固定

`blog/base.html`19行目

```py
style="position:sticky; top:0
```



### 6.苦労したこと

1.  トップページのカテゴリー検索で、初期値カテゴリーがAだったとして、カテゴリーBを選択して検索すると、検索後のページでプルダウンが初期値のカテゴリーAに戻ってしまう  
     → get_context_data を使って今選択して選んだカテゴリー項目を "selected_category" に保存させ、それをhtmlに記述

`blog/views.py`69行目

```py
context["selected_category"] = (self.request.GET.get("query_cate"))
```

`blog/post_list.html`40行目

```py
{% if item.id == selected_category %}
                    <option selected value="{{ item.id }}">{{ item.name }}</option>
```



2. 　いいねボタン押した状態でリロードすると、いいねしたときに点くcssの色が消えるため、「もし、ログインユーザーがいいねしていたらボタンのcssをオンにする」という記述をしました。  

`blog/post_list.html`93行目

```py
<button class="like-btn {% if request.user in post.like.all %}on{% endif %}"
```



3. コメント機能にユーザーIDを持たせようとモデルCommentを改修してたら、デフォルト値を求めるエラー発生

```
You are trying to add a non-nullable field ‘accessuser’ to comment without a default; we can’t do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
 ```

 シェルでCommentモデルを削除して再migrate実行

```
 python manage.py shell
from blog.models import Comment
Comment.objects.all().delete()
```

エラー変わらず。。。ここでロールバックというモデル初期化機能を知ったため、実行

```
python manage.py showmigrations blog
python manage.py migrate blog ◯◯◯　←　ロールバック処理
migrationsから今ロールバックしたファイルを全て削除
再びmakemigrations migrate実行
エラー解消！
```



4. context["selected_tag"]にrequest.GET.getで値を渡す時、値が空っぽなのでintに変換できずエラーになる

```
int() argument must be a string, a bytes-like object or a number, not 'NoneType'
```

request.GET.getが空の時は、問題のない値0を渡すようにして、変換エラーを回避

`blog/views.py`72行目

```py
context["selected_tag"] = int(self.request.GET.get("query_tag", 0))
```



5. テスト実行時、エラー AssertionError: 301 != 200 になる。コードが間違えてると思ったが原因はsettings.pyだった。

`pj_blog/settings.py`105行目

```py
 #Trueでリクエストの全てをhttpsに変える。テスト時はhttp通信のため、Falseにしないとエラーになる
SECURE_SSL_REDIRECT = False
```



6. 会員登録フォームに入力して仮登録した時、メールサーバーエラーなどが発生して認証メールが送れなかったのに、データベースにユーザーデータが登録されてしまう。  
    → 例外(エラーなど)発生時、今登録したユーザーデータを自動で削除

`registration/forms.py`51行目

```py
if commit:
            user.save() # 本セーブする
            activate_url = get_activate_url(user)
            message = message_template + activate_url
            try:
                user.email_user(subject, message) # email_userメソッドでuserにメールをtry(送信)する

            # 例外処理
            except Exception as e:
                user.delete() # エラーが起きた場合、今登録したデータを削除
        return user # このuserはUserオブジェクト
```
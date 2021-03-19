<<<<<<< HEAD

=======
# Python/Djangoでブログアプリを作成しました

## 目次

1.アプリの概要  
2.作ろうと思った理由  
3.実装した機能  
4.工夫した点  
5.苦労したこと  
6.常に意識したこと

### 1.アプリの概要

このアプリは、現在ぼっちで寂しい思いをしてる人達が最近あった悲しい出来事などをブログ形式で投稿し、それを会員同士で共有できるコミュニティです。  
ユーザー同士で投稿されたブログに対して「いいね」を付けあったりできるので、人気の記事がわかりやすいです。また、高評価を得るよう投稿内容のクオリティやモチベーションを高められます。  
また、検索機能もあるので見たいブログを素早く見つけられます。

### 2.作ろうと思った理由

社会問題になりつつある「ぼっち」 この寂しさは経験者にしかわかりません。そこで、ぼっち経験者のみが集まるコミュニティを作って仲間同士で盛り上がれるコミュニティがあると良いなと思ったので作ってみました。


### 3.実装した機能

インフラにherokuを使用  
新規会員登録、ログイン、ログアウト、パスワード変更、会員情報変更  
CRUD機能   
投稿検索機能  
いいねボタン  
無限スクロール機能 

### 4.工夫した点

1.  タップ操作をなるべく減らしてユーザビリティを向上させたいと思い、ページネーションではなく無限スクロールを実装  

`blog/post_list.html`  

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

`blog/post_list.html`

```py
<button class="like-btn {% if request.user in post.like.all %}on{% endif %}"
                       data-href="{{ post.get_api_like_url }}" data-id="{{post.pk}}">
          <span class="liked-cnt" id="like{{post.pk}}">{{ post.like.count }}</span>
          <i class="fas fa-thumbs-up"></i>
    </button>
```



3.  ユーザーが探したいブログをすぐ探せるよう、さまざまなタイプの検索フォームを実装

`blog/views.py`

def get_querysetを使い、タイトル、本文からワード検索
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

4. 無限スクロールで一番下行って、もし一番上に戻りたいと思った時一発で戻れるよう、トップページリンクであるへーダーを固定

`blog/base.html`19行目

```py
style="position:sticky; top:0
```

### 5.苦労したこと

1.  トップページのカテゴリー検索で、初期値カテゴリーがAだったとして、カテゴリーBを選択して検索すると、検索後のページでプルダウンが初期値のカテゴリーAに戻ってしまう  
     → def get_context_data を使って今選択して選んだカテゴリー項目を "selected_category" に保存させ、それをhtmlに記述

`blog/views.py class Index`

```py
context["selected_category"] = (self.request.GET.get("query_cate"))
```

`blog/post_list.html`

```py
{% if item.id == selected_category %}
                    <option selected value="{{ item.id }}">{{ item.name }}</option>
```

2.　いいねボタン押した状態でリロードすると、いいねしたときに点くcssの色が消えるため、「もし、ログインユーザーがいいねしていたらボタンのcssをオンにする」という記述をしました。  

`blog/post_list.html`

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

```py
context["selected_tag"] = int(self.request.GET.get("query_tag", 0))
```

>>>>>>> 2470c7ea5d9c1226cd896a513870e3dc6b827c63

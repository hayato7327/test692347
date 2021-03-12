# Python/Djangoでブログアプリを作成しました

## 目次

1.アプリの概要  
2.作ろうと思った理由  
3.工夫した点  
4.苦労したこと  

### 1.アプリの概要

[Paiza](https://paiza.cloud)で作業している方はdjangoにチェックを入れて新規サーバーを立ち上げて下さい。  
自分のマシンで作業している方はdjangoが使える作業用フォルダを作成して下さい。

### 前回管理サイトをカスタマイズしたプロジェクトをダウンロード

ターミナルを開いて、以下を実行。

```sh
git clone https://github.com/shun-rec/django-website-13
```

フォルダを移動

```sh
cd django-website-13
```

### マイグレートしてDBを作成

```sh
python manage.py migrate
```

### スーパーユーザーを作成

```sh
python manage.py createsuperuser
```

* ユーザー名: admin
* メールアドレス: （無し）
* パスワード: admin

### 動かしてみよう

```py
python manage.py runserver
```

`/staff-admin/`にアクセスして、前回作成した管理画面が表示されればOKです。

## フィールドを変更しよう

現在はモデルの編集画面で各項目がフィールド名そのまま英語で表示されています。
これを自分で設定した日本語のものに変えましょう。

モデルの各フィールドに`verbose_name`引数で文字列を渡すことで設定する事ができます。

今回は`Post`モデルの各フィールドを日本語に変えてみましょう。

### created

まずは`Post`モデルの`created`フィールドの最後に以下のように`verbose_name="作成日"`と追加しましょう。

`blog/models.py`

```py
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        blank=False,
        null=False,
        verbose_name="作成日"
    )
```

同じ要領ですべてのフィールドの最後に`verbose_name`を追加しましょう。

### updated

```py
        verbose_name="最終更新日"
```

### title

```py
        verbose_name="タイトル"
```

### body

```py
        verbose_name="本文",
```

### category

```py
        verbose_name="カテゴリ"
```

### tags

```py
        verbose_name="タグ"
```

### published

```py
        verbose_name="公開する"
```

### 動かしてみよう

Post編集ページで各項目が今設定したものに変わっていればOKです。

## フィールドにユーザーのヘルプ文言を表示しよう

項目の入力に説明がないと不親切なときはユーザーにヘルプ文言を表示しましょう。

モデルのフィールドに`help_text`で文字列を渡すことで設定できます。

今回は本文に「HTMLタグは使えません。」というヘルプ文言を表示してみましょう。

`blog/models.py`の`Post`モデルの`body`フィールドの最後に以下を追記します。

```py
        help_text="HTMLタグは使えません。"
```

## 表示するフィールドを制御しよう

編集ページで非表示にしたい項目があることがあります。  
その場合には`AdminModel`に`fields`を指定することで表示される項目を選択することが出来ます。  
デフォルトでは、編集可能な項目はすべて表示されます。

今回は一時的にタイトルだけが表示されるようにしてみましょう。

`blog/admin.py`の`PostAdmin`の先頭に以下を追記しましょう。  
タプルな要素１つの場合末尾に`,`をつける必要があることに注意して下さい。

```py
    fields = ('title',)
```

タイトルだけが表示できたことが確認出来たら、表示をもとに戻しましょう。

```py
    fields = ('title', 'body', 'category', 'tags')
```

## 編集不可な項目を表示しよう

編集な出来なくても項目の表示だけはしたいことがあります。  
`readonly_fields`にフィールド名を指定することで表示できます。  
注意点として、`fields`に指定されていないフィールドの場合は`fields`にも追加が必要です。

`blog/admin.py`の`PostAdmin`の先頭を以下のように書き換えましょう。

```py
    readonly_fields = ('created', 'updated')
    fields = ('title', 'body', 'category', 'tags', 'created', 'updated')
```

## フォームのフィールドを分類しよう

項目を分かりやすく分類して表示するには`fieldsets`を使います。  
指定の仕方が複雑なので以下のサンプルを参考にして下さい。  
分類をタプルのリストで表現します。  
タプルの1つ目の要素に分類のタイトルを2つ目の要素にその分類に入れる項目を指定します。  
タイトルは`None`にするとヘッダが非表示になります。
注意点として、`fieldsets`を使用する際には`fields`は削除します。

今回は以下のように分類してみます。  
`blog/admin.py`の`PostAdmin`の`fields`を削除して、`readonly_fields`の下に以下を追記します。

```py
    fieldsets = [
        (None, {'fields': ('title', )}),
        ('コンテンツ', {'fields': ('body', )}),
        ('分類', {'fields': ('category', 'tags')}),
        ('メタ', {'fields': ('created', 'updated')})
    ]
```

## フォームのさらなるカスタマイズ

さらなるカスタマイズが必要な場合、独自のフォームを指定することも出来ます。  
モデルで共通で使うことも出来ます。

今回は項目のタイトルをさらに変更するために独自フォームを使用してみます。

`blog/admin.py`の`PostAdmin`の上に以下を追記します。

```py
from django import forms

class PostAdminForm(forms.ModelForm):
    class Meta:
        labels = {
            'title': 'ブログタイトル',
        }
```

そして、`PostAdmin`の中に`form`を追記して先程作ったフォームを指定します。

```py
    form = PostAdminForm
```

フォームについて詳細は第７回、第８回を参照して下さい。

## バリデーションの追加

普通はモデルに追加するのが良いことが多いです。  
それが出来ない場合はFormに追加することも出来ます。

今回は本文にHTMLタグが使われていたらエラーが表示されるようにします。

`blog/admin.py`の`PostAdminForm`のメソッドとして以下を追記します。

```py
    def clean(self):
        body = self.cleaned_data.get('body')
        if '<' in body:
            raise forms.ValidationError('HTMLタグは使えません。')
```

## 多対多フィールドを選択しやすくしよう

`Post`のタグのようにManyToManyフィールドはデフォルトでは選択しにくいものになっています。  
これを左に未選択のもの、右に選択中のもの、と分かりやすくしてみます。  
`filter_horizontal`に対象のManyToManyフィールド名を指定します。

今回はタグをそのように変更してみます。  

`blog/admin.py`の`PostAdmin`の`form`の下に以下を追記します。

```py
    filter_horizontal = ('tags',)
```

## 関連モデルも同時に修正 - インライン

ForeignKeyフィールドやOneToOneフィールドを使っている場合に、関連するモデルも一緒に編集したいことがあります。  
１つのページに関連する２つ以上モデルを表示するには`inline`というものを使用します。

今回はカテゴリ編集ページにそのカテゴリのブログ一覧を表示してみます。

### インラインクラスの追加

`blog/admin.py`の`CategoryAdmin`の上に以下のクラスを追加します。

```py
class PostInline(admin.TabularInline):
    model = models.Post
    fields = ('title', 'body')
    extra = 1
```

* インラインを作るには`admin.TabularInline`というクラスを継承します
* modelに表示するモデルを指定します
* fieldsに編集させるフィールドを列挙します
* extraに新規追加用の空白フォームの数を指定します

### 自作のインラインクラスを指定

今作ったインラインクラスを指定するには、`inline`という配列に追加します。

`blog/admin.py`の`CategoryAdmin`の中に以下を追記します。

```py
    inlines = [PostInline]
```

## 保存時に処理を追加

データの保存前後に独自の処理を入れたいことがあります。  
例えばデフォルトのタグを追加したりなどです。

その場合には`save_model`メソッドを上書きします。

今回は保存の前後に`print`分でログの表示だけをしてみましょう。

`blog/admin.py`の`PostAdmin`に以下を追記します。  
`print`文のところに独自の処理を入れるとそれが実行されます。

```
    def save_model(self, request, obj, form, change):
        print("before save")
        super().save_model(request, obj, form, change)
        print("after save")
```

## 新規作成フォームと編集フォームのテンプレートの上書き

`change_form.html`というファイルを上書きすることで、編集ページのデザインを変更することが出来ます。  
どこにこのファイルを置くかでデザインの適用範囲が変わってきます。  

* admin直下: 全モデル。
* admin/<アプリ名>/: 特定のアプリのみ
* admin/<アプリ名>/<モデル名>/: 特定のモデルのみ

今回は、以下のような注意書きをページ先頭に追加してみます。

* ブログ編集ページ: 「すべてのフィールドが必須です。」
* その他のページ: 「カテゴリ、タグの追加・編集は管理者のみ行って下さい」

まずはその他のページから。

Postモデル以外すべてに適用したいので、`templates/admin/blog/`以下に配置します。

`templates/admin/blog/change_form.html`

```html
{% extends "admin/change_form.html" %}

{% block content %}
    <h2>カテゴリ、タグの追加・編集は管理者のみ行って下さい。</h2>
    {{ block.super }}
{% endblock %}
```

ブログ編集ページの変更はこのページだけに適用したいので、さらに`post/`フォルダの中に配置します。

`templates/admin/blog/post/change_form.html`

```html
{% extends "admin/change_form.html" %}

{% block content %}
    <h2>すべてのフィールドが必須です。</h2>
    {{ block.super }}
{% endblock %}
```

## JSの読み込み

ページを再読み込みせずにリアルタイムに処理を行いたいことがあります。  
それにはJavascriptが必要になります。  
独自のJavascriptを読み込んでみましょう。  
djangoの管理画面ではデフォルトでjQueryが使用できるようになっています。
独自のJavascriptの中でもjQueryが使用可能です。

今回は投稿編集ページでアラートダイアログを表示してみましょう。

`static/post.js`というファイルを新規作成し、以下の内容を追記します。

```js
(function($) {
  $(document).ready(function() {
    alert("JSが読み込まれました。")
  });
})(django.jQuery || jQuery);
```

`blog/admin.py`の`PostAdmin`の中に以下のインナークラスを追加します。

```py
    class Media:
        js = ('post.js',)
```

* jsに読み込みたいJavascriptファイルを列挙します。

ページを開いた時にアラートダイアログが表示されればOKです。

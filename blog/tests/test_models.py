from django.test import TestCase
from blog.models import Post
from blog.models import Category
from blog.models import Tag



class PostModelTests(TestCase):
    
    
         #初期状態では何も登録されていないかテスト    
    def test_is_empty(self):
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)
        
        
         #レコードを１つ作成するとレコードが１つだけカウントされるかテスト
    def test_is_count_one(self):
        category = Category(name='テストカテゴリー')
        category.save()
        tag = Tag(name='テストタグ')
        tag.save()
        post = Post(category=category,title='test_title',
                    body='test_body', published=1)
        post.save()
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 1)
        
        
         #内容を指定してデータを保存し、すぐに取り出した時に
         #保存した時と同じ値が返されることをテスト
    def test_saving_retrieving_post(self):
        category = Category(name='テストカテゴリー')
        category.save()
        tag = Tag(name='テストタグ')
        tag.save()
        post = Post(category=category,title='test_title',
                    body='test_body', published=1)
        post.save()
        
        saved_posts = Post.objects.all()
        actual_post = saved_posts[0]
        
        self.assertEqual(actual_post.title, 'test_title')
        self.assertEqual(actual_post.body, 'test_body')
        self.assertEqual(actual_post.published, 1)
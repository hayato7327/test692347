from django.test import TestCase, Client
from django.urls import reverse
from registration.models import User

      #ログイン時、ユーザー名nomuraが含まれているか確認 
class Test_Login(TestCase):
    
    def test_authenticated(self):
        user = User.objects.create_user(username = 'nomura',password = 'adgjm135')
        self.client.force_login(user)
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(user.username, 'nomura')
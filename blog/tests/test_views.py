from django.test import TestCase, Client
from django.contrib.auth.models import AbstractUser


class TestViewsHome(TestCase):

    def test_not_authenticated(self):
        client = Client()
        client.logout()
        response = client.get('/')
        self.assertFalse('username' in response.context)

    def test_authenticated(self):
        client = Client()
        client.force_login(User.objects.create_user('tester'))
        response = client.get('/')
        self.assertTrue('username' in response.context)
        self.assertEqual(response.context['username'], 'tester')
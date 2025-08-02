from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus



# Create your tests here.

class HomePageTestCase(TestCase):
    fixtures = ['users_user.json']

    def setUp(self):
        pass

    def test_main_page_open(self):
        User = get_user_model()
        u = User.objects.get(pk=1)
        self.client.force_login(u)
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def tearDown(self):
        pass
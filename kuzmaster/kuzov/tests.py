from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from http import HTTPStatus



# Create your tests here.

class HomePageTestCase(TestCase):
    fixtures = ['users_user.json', 'kuzov_zakaznaryad', 'kuzov_auto', 'kuzov_client']

    def setUp(self):
        pass

    def test_main_page_open(self):
        User = get_user_model()
        u = User.objects.get(pk=1)
        self.client.force_login(u)
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('kuzov/index.html', response.template_name)
        self.assertEqual(response.context_data['title'], 'Главная страница')
    
    def test_unathorized_login_redirect(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def tearDown(self):
        pass


class ShowOrderTestCase(TestCase):
    fixtures = ['users_user.json', 'kuzov_zakaznaryad', 'kuzov_auto', 'kuzov_client']

    def setUp(self):
        pass

    def test_main_page_open(self):
        User = get_user_model()
        u = User.objects.get(pk=1)
        self.client.force_login(u)
        path = reverse('show_order', kwargs={'order_id': 1})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('kuzov/order.html', response.template_name)
#        self.assertEqual(response.context_data['title'], 'Главная страница')

    def tearDown(self):
        pass
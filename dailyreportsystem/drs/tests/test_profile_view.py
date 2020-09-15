from datetime import datetime
import pytz
import uuid
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from drs.models import User

class ProfiletViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create_user(email='testuser1@test.com', password='1X<ISRUkw+tuK', is_active=True)
        test_user1.save()

    def test_user_login(self):
        c = Client()
        login = c.post('/login/', {'email':'testuser1@test.com', 'password':'1X<ISRUkw+tuK'})
        self.assertTrue(login)

    def test_redirect_if_not_logged_in_view_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertRedirects(response, '/login/')

    def test_redirect_if_not_logged_in_view_user(self):
        response = self.client.get(reverse('profile-user'))
        self.assertRedirects(response, '/login/')

    def test_employee_access_manager_view(self):
        self.client = Client()
        self.client.login(email="testuser1@test.com", password='1X<ISRUkw+tuK')
        res = self.client.get(reverse('all_requests'))
        self.assertEqual(res.status_code, 404)

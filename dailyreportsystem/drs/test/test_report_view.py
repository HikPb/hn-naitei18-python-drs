from datetime import datetime
import pytz
import uuid
from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import Permission # Required to grant the permission needed to set a book as returned.
from drs.models import Report, Plan, User, Division

class ReportViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 13 authors for pagination tests
        number_of_forms = 13
        test_user1 = User.objects.create_user(email='testuser1@test.com', password='1X<ISRUkw+tuK', is_active=True, is_staff=True)
        test_user2 = User.objects.create_user(email='testuser2@test.com', password='1X<ISRUkw+tuK', is_active=True, is_staff=True, is_manager=True)
        division = Division.objects.create(name='Test Division', manager=test_user2)
        plan = Plan.objects.create(title='test project')

        test_user1.save()
        test_user2.save()
        division.save()
        plan.save()

        # create report
        created_at = datetime(2020, 9, 15, 12, 0, 0, 0, tzinfo=pytz.UTC)
        # Report.objects.create(receiver=test_user2, sender=test_user1, created_at=created_at,
        #                       division=division, plan=plan, actual='unit test', next='done', issue='no')

        for report_id in range(number_of_forms):
            Report.objects.create(
                receiver=test_user2,
                sender=test_user1,
                created_at=created_at,
                division=division,
                plan=plan,
                actual='unit test',
                next='done',
                issue='no')

    def test_user_login(self):
        c = Client()
        login = c.post('/login/', {'email':'testuser1@test.com', 'password':'1X<ISRUkw+tuK'})
        self.assertTrue(login)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('reports'))
        self.assertRedirects(response, '/login/')

    def test_logged_in_uses_correct_template(self):
        c = Client()
        c.post('/login/', {'email':'testuser1@test.com', 'password':'1X<ISRUkw+tuK'})
        response = c.get(reverse('reports'))
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

    def test_not_owner_user_delete_event(self):
        c = Client()
        c.post('/login/', {'email':'testuser2@test.com', 'password':'1X<ISRUkw+tuK'})
        c.post(reverse('report_delete', kwargs={'pk':13}))
        check = Report.objects.filter(id=13).exists()
        self.assertTrue(check)

    def test_report_owner_delete_event(self):
        self.client = Client()
        self.client.login(email="testuser1@test.com", password='1X<ISRUkw+tuK')
        item = Report.objects.get(id=13)
        url = reverse('report_delete', kwargs={'pk':item.id})
        self.client.post(url)
        check = Report.objects.filter(id=13).exists()
        self.assertFalse(check)

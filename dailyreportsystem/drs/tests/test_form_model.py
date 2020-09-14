from django.test import TestCase
from datetime import datetime
import pytz
from drs.models import Form, User, Division

class FormModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user1 = User.objects.create_user(email='testuser1@test.com', password='1X<ISRUkw+tuK')        
        test_user2 = User.objects.create_user(email='testuser2@test.com', password='1X<ISRUkw+tuK')
        division = Division.objects.create(name='Test Division', manager=test_user2)
        test_user1.save()
        test_user2.save()
        division.save()
        created_at = datetime(2020, 9, 15, 12, 0, 0, 0, tzinfo=pytz.UTC)
        compensation_from = datetime(2020, 9, 15, 17, 0, 0, tzinfo=pytz.UTC)
        compensation_to = datetime(2020, 9, 15, 18, 0, 0, tzinfo=pytz.UTC)
        checkin = datetime(2020, 9, 15, 8, 0, 0, tzinfo=pytz.UTC)
        Form.objects.create(title='form test', receiver=test_user2, sender=test_user1, created_at=created_at, division=division, content='test',
                            compensation_from=compensation_from, compensation_to=compensation_to, checkin_time=checkin, form_type='il')

    def test_form_title_label(self):
        form = Form.objects.get(id=1)
        field_label = Form._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_form_receiver_label(self):
        form = Form.objects.get(id=1)
        field_label = Form._meta.get_field('receiver').verbose_name
        self.assertEquals(field_label, 'receiver')
    
    def test_form_sender_label(self):
        form = Form.objects.get(id=1)
        field_label = Form._meta.get_field('sender').verbose_name
        self.assertEquals(field_label, 'sender')
    
    def test_form_division_label(self):
        form = Form.objects.get(id=1)
        field_label = Form._meta.get_field('division').verbose_name
        self.assertEquals(field_label, 'division')
    
    def test_form_content_label(self):
        form = Form.objects.get(id=1)
        field_label = Form._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')

    def test_form_status_label(self):
        form = Form.objects.get(id=1)
        field_label = Form._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'status')

    def test_title_max_length(self):
        form = Form.objects.get(id=1)
        max_length = Form._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_content_max_length(self):
        form = Form.objects.get(id=1)
        max_length = Form._meta.get_field('content').max_length
        self.assertEquals(max_length, 1000)

    def test_default_status(self):
        form = Form.objects.get(id=1)
        df = Form._meta.get_field('status').default
        self.assertEquals(df, 'p')

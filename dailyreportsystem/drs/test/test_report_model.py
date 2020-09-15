from django.test import TestCase
from datetime import datetime
import pytz
from drs.models import Report, Plan ,User, Division

class PlanModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Plan.objects.create(title='test project')

    def test_title_max_length(self):
        plan = Plan.objects.get(id=1)
        max_length = plan._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    # def test_get_absolute_url(self):
    #     plan = Plan.objects.get(id=1)
    #     # This will also fail if the urlconf is not defined.
    #     self.assertEquals(plan.get_absolute_url(), '/drs/plan/1')

class ReportModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Create two users
        test_user1 = User.objects.create_user(email='testuser1@test.com', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(email='testuser2@test.com', password='1X<ISRUkw+tuK')
        division = Division.objects.create(name='Test Division', manager=test_user2)
        plan = Plan.objects.create(title='test project')

        test_user1.save()
        test_user2.save()
        division.save()
        plan.save()

        #create report
        created_at = datetime(2020, 9, 15, 12, 0, 0, 0, tzinfo=pytz.UTC)
        Report.objects.create(receiver=test_user2, sender=test_user1, created_at=created_at,
                              division=division,plan= plan, actual='unit test',next= 'done',issue ='no')

    def test_report_receiver_label(self):
        report = Report.objects.get(id=1)
        field_label = report._meta.get_field('receiver').verbose_name
        self.assertEquals(field_label, 'receiver')

    def test_report_sender_label(self):
        report = Report.objects.get(id=1)
        field_label = report._meta.get_field('sender').verbose_name
        self.assertEquals(field_label, 'sender')

    def test_report_division_label(self):
        report = Report.objects.get(id=1)
        field_label = report._meta.get_field('division').verbose_name
        self.assertEquals(field_label, 'division')

    def test_report_plan_label(self):
        report = Report.objects.get(id=1)
        field_label = report._meta.get_field('plan').verbose_name
        self.assertEquals(field_label, 'plan')

    def test_report_actual_label(self):
        report = Report.objects.get(id=1)
        field_label = report._meta.get_field('actual').verbose_name
        self.assertEquals(field_label, 'actual')

    def test_report_next_label(self):
        report = Report.objects.get(id=1)
        field_label = report._meta.get_field('next').verbose_name
        self.assertEquals(field_label, 'next')

    def test_report_issue_label(self):
        report = Report.objects.get(id=1)
        field_label = report._meta.get_field('issue').verbose_name
        self.assertEquals(field_label, 'issue')

    def test_actual_max_length(self):
        report = Report.objects.get(id=1)
        max_length = report._meta.get_field('actual').max_length
        self.assertEquals(max_length, 1000)

    def test_next_max_length(self):
        report = Report.objects.get(id=1)
        max_length = report._meta.get_field('next').max_length
        self.assertEquals(max_length, 1000)

    def test_issue_max_length(self):
        report = Report.objects.get(id=1)
        max_length = report._meta.get_field('issue').max_length
        self.assertEquals(max_length, 1000)

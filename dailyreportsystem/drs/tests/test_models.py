from django.test import TestCase
from drs.models import Division, User


class TestModelDivision(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Division.objects.create(name='Hello')

    def test_name_label(self):
        division = Division.objects.get(id=1)
        field_label = division._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_manager_label(self):
        division = Division.objects.get(id=1)
        field_label = division._meta.get_field('manager').verbose_name
        self.assertEquals(field_label, 'manager')

    def test_parent_label(self):
        division=Division.objects.get(id=1)
        field_label = division._meta.get_field('parent').verbose_name
        self.assertEquals(field_label, 'parent')

    def test_name_max_length(self):
        division = Division.objects.get(id=1)
        max_length = division._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_name(self):
        division = Division.objects.get(id=1)
        expected_object_name = f'{division.name}'
        self.assertEquals(expected_object_name, str(division))

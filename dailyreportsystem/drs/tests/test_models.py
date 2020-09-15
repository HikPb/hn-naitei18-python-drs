from django.test import TestCase
from drs.models import Division, User, Plan, Position, Skill


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


class TestModelPlan(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Plan.objects.create(title='Hiii')

    def test_title_label(self):
        plan = Plan.objects.get(id=1)
        field_label = plan._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_title_max_length(self):
        plan = Plan.objects.get(id=1)
        max_length = plan._meta.get_field('title').max_length
        self.assertEquals(max_length, 100)

    def test_object_title_is_title(self):
        plan = Plan.objects.get(id=1)
        expected_object_title = f'{plan.title}'
        self.assertEquals(expected_object_title, str(plan))


class TestModelSkill(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Skill.objects.create(name='AhihiHiii')

    def test_name_label(self):
        skill = Skill.objects.get(id=1)
        field_label = skill._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        skill = Skill.objects.get(id=1)
        max_length = skill._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_name(self):
        skill = Skill.objects.get(id=1)
        expected_object_name = f'{skill.name}'
        self.assertEquals(expected_object_name, str(skill))


class TestModelPosition(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Position.objects.create(name='AhihiHiii')

    def test_name_label(self):
        position = Position.objects.get(id=1)
        field_label = position._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        position = Position.objects.get(id=1)
        max_length = position._meta.get_field('name').max_length
        self.assertEquals(max_length, 50)

    def test_object_name_is_name(self):
        position = Position.objects.get(id=1)
        expected_object_name = f'{position.name}'
        self.assertEquals(expected_object_name, str(position))

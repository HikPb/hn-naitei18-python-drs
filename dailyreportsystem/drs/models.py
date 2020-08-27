from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from PIL import Image

class CustomUserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(email=self.normalize_email(email), **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self, email, password, **extra_fields):
		"""
		Creates and saves a staff user with the given email and password.
		"""
		extra_fields.setdefault('is_staff', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		return self.create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		"""
		Create and save a SuperUser with the given email and password.
		"""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	"""Custom for User Model"""
	objects = CustomUserManager()
	email = models.EmailField(
		verbose_name='email address',
		max_length=255,
		unique=True,
	)
	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	# notice the absence of a "Password field", that is built in.
	name = models.CharField(max_length=50, null=True)
	dob = models.DateField(null=True, blank=True)
	phone = models.CharField(max_length=11, null=True, blank=True)
	skill = models.ManyToManyField('Skill', help_text="Your skills", blank=True)
	manager = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='manager_user')
	division = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True, blank=True)
	position = models.ForeignKey('Position', on_delete=models.SET_NULL, null=True, blank=True)
	sex =  models.CharField(max_length=50, null=True, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []  # Email & Password are required by default.

	def __str__(self):              # __unicode__ on Python 2
		return self.email


# class Sex(models.Model):


class Form(models.Model):
	"""dsfas"""
	# Fields
	title = models.CharField(max_length=200)
	receiver = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='receiver_form')
	sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender_form')
	created_at = models.DateTimeField(null=True, blank=True)
	division = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True)
	content = models.TextField(max_length=1000, null=False)
	compensation_from = models.DateTimeField(null=False)
	compensation_to = models.DateTimeField(null=False)
	leave_from = models.DateTimeField(null=True, blank=True)
	leave_to = models.DateTimeField(null=True, blank=True)
	checkin_time = models.DateTimeField(null=True, blank=True)
	checkout_time = models.DateTimeField(null=True, blank=True)

	FORM_TYPE = (
		('le', 'Leave Early'),
		('lo', 'Leave Out'),
		('il', 'In Late'),
	)

	form_type = models.CharField(
		max_length=2,
		choices=FORM_TYPE,
		help_text='Form type',
	)

	FORM_STATUS = (
		('a', 'Approved'),
		('c', 'Canceled'),
		('f', 'Forwarded'),
		('p', 'Pending'),
		('r', 'Rejected'),
	)

	status = models.CharField(
		max_length=1,
		choices=FORM_STATUS,
		default='p',
		help_text='Form status',
	)
	# Methods

	class Meta:
		ordering = ['created_at']

	def get_absolute_url(self):
		"""Returns the url to access a particular instance of MyModelName."""
		return reverse('form', args=[str(self.id)])

	def __str__(self):
		"""String for representing the MyModelName object (in Admin site etc.)."""
		return self.title


class Report(models.Model):
	"""dsfas"""
	# Fields
	sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender_report')
	receiver = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='receiver_report')
	created_at = models.DateTimeField(null=True, blank=True)
	division = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True)
	plan = models.TextField(max_length=1000)
	actual = models.TextField(max_length=1000)
	next = models.TextField(max_length=1000)
	issue = models.TextField(max_length=1000, null=True)

	# Methods
	def get_absolute_url(self):
		"""Returns the url to access a particular instance of MyModelName."""
		return reverse('report', args=[str(self.id)])

	def __str__(self):
		"""String for representing the MyModelName object (in Admin site etc.)."""
		return self.plan


class Notification(models.Model):
	""" Notification """
	# Fields
	created_at = models.DateTimeField(null=True, blank=True)
	receiver = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='receiver')
	sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender')
	is_read = models.BooleanField(default=False)
	form_id = models.ForeignKey('Form', on_delete=models.CASCADE, null=True)
	type_notification = models.CharField(max_length=50)
	content = models.CharField(max_length=50)

	class Meta:
		ordering = ['created_at']

	# Methods
	def get_absolute_url(self):
		return reverse('notification', args=[str(self.id)])

	def __str__(self):
		return self.content


class Skill(models.Model):
	""" Model of Genre """
	# Fields
	name = models.CharField(max_length=50, help_text='Enter a skill (e.g. Python)')
	# Methods

	def __str__(self):
		return self.name


class Position(models.Model):
	"""Position"""
	name = models.CharField(max_length=50, help_text='Enter your position (e.g. Deverloper)')
	# Method

	def __str__(self):
		return self.name


class Division(models.Model):
	"""Division"""
	name = models.CharField(max_length=50, help_text='Enter your division (e.g. Education Team)')
	manager = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='manager_div')
	parent_id = models.ForeignKey('Division', on_delete=models.SET_NULL, null=True, blank=True)
	# Method

	def __str__(self):
		return self.name


class TimeKeeping(models.Model):
	"""Model Timekeeping"""
	user_id = models.ForeignKey('User', on_delete=models.CASCADE, null=True)
	checkin_time = models.DateTimeField(null=True, blank=True)
	checkout_time = models.DateTimeField(null=True, blank=True)
	date = models.DateField(null=True, blank=True)


class Profile(models.Model):
	user = models.OneToOneField('User', on_delete=models.CASCADE, null=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.email} Profile'

	def display_skill(self):
		"""Creates a string for the Genre. This is required to display genre in Admin."""
		return ', '.join([skill.name for skill in self.skill.all()[:3]])

	display_skill.short_description = 'Skill'

	def save(self):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)

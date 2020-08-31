from .models import CustomUserManager, User, Form, Report, Notification, Skill, Position, Division, TimeKeeping
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .serializers import FormSerializer, ReportSerializer
from rest_framework import viewsets
from django.contrib import messages
from django.utils.translation import ugettext as _

UserModel = get_user_model()


def index(request):
	"""View function for home page of site."""
	if not request.user.is_authenticated:
		return redirect(reverse_lazy('login-user'))
	email = request.user
	# Generate counts of some of the main objects
	context = {
		'email': email,
	}
	return render(request, 'index.html', context=context)


def loginUser(request):
	if request.user.is_authenticated:
		return redirect(reverse_lazy('home'))
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')

		user = authenticate(request, email=email, password=password)

		if user is not None:
			login(request, user)
			messages.success(request, _('You are logged in sucessfully!!!'))
			return redirect('home')
		else:
			messages.info(request, _('username or password is incorrect'))

	context = {
	}
	return render(request, '../templates/sign_up/login.html', context)


def logoutUser(request):
	logout(request)
	messages.success(request, _('You are logged out'))
	return redirect('login-user')


def changepassword(request):
	if not request.user.is_authenticated:
		return redirect('/')
	'''
	Please work on me -> success & error messages & style templates
	'''
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			update_session_auth_hash(request, user)

			messages.success(request, 'Password changed successfully',
							 extra_tags='alert alert-success alert-dismissible show')
			return redirect('changepassword')
		else:
			messages.error(request, 'Error,changing password', extra_tags='alert alert-warning alert-dismissible show')
			return redirect('changepassword')

	form = PasswordChangeForm(request.user)
	return render(request, '../templates/sign_up/password_reset_form.html', {'form': form})


class FormDetailView(generic.DetailView):
	"""Generic class-based detail view for a book."""
	model = Form
	template_name = "formrequest/form_detail.html"


def getMyForms(request):
	return render(request, 'formrequest/list_form_request_employee.html')


def getFormRequest(request):
    return render(request, 'formrequest/list_form_request_manager.html')
    
class MyForms(viewsets.ModelViewSet):
    # queryset = Form.objects.filter(form_type="il")
	serializer_class = FormSerializer
	def get_queryset(self):
		return Form.objects.filter(sender=self.request.user)

class FormRequest(viewsets.ModelViewSet):
	serializer_class = FormSerializer
	def get_queryset(self):
		return Form.objects.filter(receiver=self.request.user)

class FormCreateView(LoginRequiredMixin, CreateView):
	login_url = 'login-user'
	redirect_field_name = 'redirect_to'
	model = Form
	template_name = 'formrequest/form_request.html'
	fields = (
	'title', 'content', 'form_type', 'compensation_from', 'compensation_to', 'leave_from', 'leave_to', 'checkin_time',
	'checkout_time')
	success_url = reverse_lazy('my_forms')

	def form_valid(self, form):
		if self.request.user.is_authenticated:
			form.instance.user = self.request.user
		form.instance.receiver = self.request.user.manager
		form.instance.sender = self.request.user
		form.instance.division = self.request.user.division
		form.instance.created_at = timezone.now()
		return super(FormCreateView, self).form_valid(form)

	def form_invalid(self, form):
		"""If the form is invalid, render the invalid form."""
		return redirect(reverse_lazy('my_forms'))

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		self.object = None
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)


class FormUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Form
	template_name = 'formrequest/update_form_request.html'
	fields = ('title', 'content', 'form_type', 'compensation_from', 'compensation_to',
			  'leave_from', 'leave_to', 'checkin_time', 'checkout_time', 'status')
	success_url = reverse_lazy('my_forms')

	def test_func(self):
		if (self.get_object().status == 'p') and (self.get_object().sender == self.request.user):
			return True
		return False


class FormDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Form
	template_name = 'formrequest/form_confirm_delete.html'
	success_url = reverse_lazy('my_forms')
	def test_func(self):
		if self.get_object().status == 'p':
			return True
		return False

class ManagerChangeForm(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Form
	template_name = 'formrequest/approval_manager.html'
	fields = ('status',)
	success_url = reverse_lazy('all_requests')
	def test_func(self):
		if (self.get_object().status != 'r') and (self.get_object().status != 'a') and (self.get_object().receiver == self.request.user):
			return True
		return False

@login_required
def profile(request):
	return render(request, 'profile/profile.html')


def getListReport(request):
	return render(request, 'report/list_report.html')


def getListReportManager(request):
	return render(request, 'report/manager_list_report.html')


class ListReport(viewsets.ModelViewSet):
	serializer_class = ReportSerializer

	def get_queryset(self):
		return Report.objects.filter(sender=self.request.user)


class ListReportManager(viewsets.ModelViewSet):
	serializer_class = ReportSerializer

	def get_queryset(self):
		return Report.objects.filter(receiver=self.request.user)

class ReportCreateView(LoginRequiredMixin, CreateView):
	model = Report
	login_url = 'login-user'
	redirect_field_name = 'redirect_to'
	template_name = 'report/report_create.html'
	fields = ('plan', 'actual', 'issue', 'next')
	success_url = reverse_lazy('reports')

	def form_valid(self, report):
		if self.request.user.is_authenticated:
			report.instance.sender = self.request.user
			report.instance.receiver = self.request.user.manager
			report.instance.division = self.request.user.division
			report.instance.created_at = timezone.now()
		return super(ReportCreateView, self).form_valid(report)

	def form_invalid(self, form):
		"""If the form is invalid, render the invalid form."""
		return redirect(reverse_lazy('report_create'))

	def post(self, request, *args, **kwargs):
		report = self.get_form()
		self.object = None
		if report.is_valid():
			return self.form_valid(report)
		else:
			return self.form_invalid(report)

class ReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Report
	template_name = 'report/report_update.html'
	fields = ('plan', 'actual', 'issue', 'next')
	success_url = reverse_lazy('reports')

	def test_func(self):
		if self.get_object().sender == self.request.user:
			return True
		return False


class ReportDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Report
	template_name = 'report/report_confirm_delete.html'
	success_url = reverse_lazy('reports')
	def test_func(self):
		# if self.get_object().sender == self.request.user:
		# 	return True
		# return False
		return True
def profiletUser(request):
	return render(request, 'profile.html')

@login_required
def profile_update(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES,
								   instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, f'Your account has been updated')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		'u_form': u_form,
		'p_form': p_form
	}

	return render(request, 'profile/profile_update.html', context)

def success_activation(request):
	return render(request, '../templates/sign_up/verification_success.html')


def fail_activation(request):
	return render(request, '../templates/sign_up/verification_fail.html')


def inform(request):
	return render(request, '../templates/sign_up/inform_to_verify.html')


@staff_member_required
def register(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your account.'
			message = render_to_string('../templates/sign_up/acc_active_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': default_token_generator.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
				mail_subject, message, to=[to_email],
			)
			email.content_subtype = "html"
			email.send()
			return HttpResponseRedirect(reverse('inform'))
	else:
		form = SignUpForm()
	return render(request, '../templates/sign_up/register.html', {'form': form})


def activate(request, uidb64, token):
	try:
		uid = urlsafe_base64_decode(uidb64).decode()
		user = UserModel._default_manager.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and default_token_generator.check_token(user, token):
		user.is_active = True
		user.save()
		return HttpResponseRedirect(reverse('success_activation'))
	else:
		return HttpResponseRedirect(reverse('fail_activation'))

def about_us(request):
	return render(request, 'about_us.html')

def division_view(request):
	return render(request, 'division/division_view.html')

def notifications_as_read(request):
	Notification.objects.all()
	return JsonResponse({
		'status': True,
		'message': "Marked all notifications as read"
    })

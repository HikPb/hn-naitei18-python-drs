from .models import CustomUserManager, User, Form, Report, Notification, Skill, Position, Division, TimeKeeping
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SignUpForm

UserModel = get_user_model()


def index(request):
	"""View function for home page of site."""
	email = request.user
	# Generate counts of some of the main objects
	context = {
		'email': email,
	}
	return render(request, 'index.html', context=context)


def loginUser(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')

		user = authenticate(request, email=email, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, _('username or password is incorrect'))

	context = {
	}
	return render(request, 'login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login-user')


class FormDetailView(generic.DetailView):
	"""Generic class-based detail view for a book."""
	model = Form


class ListFormRequestEmployee(LoginRequiredMixin, generic.ListView):
	model = Form
	template_name = '/formrequest/list_form_request_employee.html'
	fields = '__all__'
	paginate_by = 10

# def get_queryset(self):
#     return Form.objects.filter(sender=self.request.user)


class FormCreateView(LoginRequiredMixin, CreateView):
	model = Form
	template_name = 'formrequest/form_form.html'
	fields = '__all__'


class FormUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Form
	template_name = 'formrequest/form_form.html'
	fields = '__all__'

	def test_func(self):
		if (self.get_object().status == 'p') and (self.get_object().sender == self.request.user):
			return True
		return False


class FormDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Form
	success_url = '/'
	template_name = 'formrequest/form_confirm_delete.html'

	def test_func(self):
		if self.get_object().status == 'p':
			return True
		return False


def profiletUser(request):
	return render(request, 'profile.html')


def success_activation(request):
	return render(request, 'sign_up/verification_success.html')


def fail_activation(request):
	return render(request, 'sign_up/verification_fail.html')


def inform(request):
	return render(request, 'sign_up/inform_to_verify.html')

def register(request):
	if request.method == 'GET':
		return render(request, 'login.html')
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your account.'
			message = render_to_string('sign_up/acc_active_email.html', {
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
	return render(request, 'sign_up/register.html', {'form': form})


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

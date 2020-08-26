from .models import CustomUserManager, User, Form, Report, Notification, Skill, Position, Division, TimeKeeping
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SignUpForm
from django_datatables_view.base_datatable_view import BaseDatatableView
from .models import Form, User
from .serializers import FormSerializer
from django.core import serializers
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
        'email' : email,
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
    template_name= "formrequest/form_detail.html"

def getMyForms(request):
    return render(request, 'formrequest/list_form_request_employee.html')

def getFormRequest(request):
    return render(request, 'formrequest/list_form_request_employee.html')
    
class MyForms(viewsets.ModelViewSet):
    queryset = Form.objects.all()
    serializer_class = FormSerializer

class FormRequest(viewsets.ModelViewSet):
    queryset = Form.objects.filter(status='p').order_by('created_at')
    serializer_class = FormSerializer

class FormCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login-user'
    redirect_field_name = 'redirect_to'
    model = Form
    template_name = 'formrequest/form_request.html'
    fields = ('title', 'content', 'form_type', 'compensation_from', 'compensation_to', 'leave_from', 'leave_to', 'checkin_time', 'checkout_time')
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

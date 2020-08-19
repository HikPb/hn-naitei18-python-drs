from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Form
from django.contrib import messages
from django.utils.translation import ugettext as _

def index(request):
    """View function for home page of site."""
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

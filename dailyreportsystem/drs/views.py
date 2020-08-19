from django.shortcuts import render, redirect
from django.views import generic
from table.views import FeedDataView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import CustomUserCreationForm
from .models import Form
from .tables import RequestFormTable
from django.contrib import messages

def index(request):
    """View function for home page of site."""
    email = request.user
    # Generate counts of some of the main objects
    context = {
        'email' : email,
        'name': 'Pham Ngoc Ba',
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
            messages.info(request, 'username or password is incorrect')

    context = {
    }
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

class ListRequestFormEmployee(FeedDataView):
    token = RequestFormTable.token
    def get_queryset(self):
        return super(ListRequestFormEmployee, self).get_queryset().filter(id__gt=5)

class FormCreateView(LoginRequiredMixin, CreateView):
    model = Form
    template_name = 'requestform/form_form.html'
    fields = '__all__'

class FormUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Form
    template_name = 'requestform/form_form.html'
    fields = '__all__'

    def test_func(self):
        if self.get_object().status == 'p':
            return True
        return False


class FormDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Form
    success_url = '/'
    template_name = 'requestform/form_confirm_delete.html'

    def test_func(self):
        if self.get_object().status == 'p':
            return True
        return False

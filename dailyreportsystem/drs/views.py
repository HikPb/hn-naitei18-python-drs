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
    return redirect('login')

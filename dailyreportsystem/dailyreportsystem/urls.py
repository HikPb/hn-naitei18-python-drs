"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include as incR
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from rest_framework import routers
from django.conf.urls.static import static
from drs import views

router = routers.DefaultRouter()
router.register(r'myforms', views.MyForms,basename='form_user_view')
router.register(r'allrequests', views.FormRequest,basename='form_manager_view')
router.register(r'listreports', views.ListReport, basename='report_user_view')
router.register(r'managerlistreports', views.ListReportManager, basename='report_user_view')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^api/', incR(router.urls)),
    path('drs/', include('drs.urls')),
    path('', RedirectView.as_view(url='drs/')),
    path('login/', views.loginUser, name='login-user'),
    path('logout/', views.logoutUser, name='logout-user'),
    path('profile/', views.profiletUser, name='profile-user'),
    path('about_us/', views.about_us, name='about_us'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

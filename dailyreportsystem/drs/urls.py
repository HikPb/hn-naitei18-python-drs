from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('myforms/', views.getMyForms, name='my_forms'),
    path('requestforms/', views.getFormRequest, name='all_requests'),
    path('requestform/<int:pk>/', views.FormDetailView.as_view(), name='form_detail'),
    path('requestform/create/', views.FormCreateView.as_view(), name='form_create'),
    path('requestform/<int:pk>/update/', views.FormUpdateView.as_view(), name='form_update'),
    path('allforms/<int:pk>/update/', views.ManagerChangeForm.as_view(), name='manager_change_form'),
    path('requestform/<int:pk>/delete/', views.FormDeleteView.as_view(), name='form_delete'),
    path('reports/', views.getListReport, name='reports'),
    path('managerreports/', views.getListReportManager, name='manager_reports'),
    path('report/create/', views.ReportCreateView.as_view(), name='report_create'),
    path('report/<int:pk>/update/', views.ReportUpdateView.as_view(), name='report_update'),
    path('report/<int:pk>/delete/', views.ReportDeleteView.as_view(), name='report_delete'),
    path('register/', views.register, name='register'),
    path('register/inform/', views.inform, name='inform'),
    path('register/success_activation/', views.success_activation, name='success_activation'),
    path('register/fail_activation/', views.fail_activation, name='fail_activation'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
    path('division_view/', views.division_view, name='division_view'),
    path('notifications-as-read', views.notifications_as_read, name="notifications-as-read"),
    path('change-password/',views.changepassword,name='changepassword'),
]

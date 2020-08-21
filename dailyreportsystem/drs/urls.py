from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('myforms/', views.ListFormRequestEmployee.as_view(), name='my_forms'),
    path('requestform/<int:pk>/', views.FormDetailView.as_view(), name='form_detail'),
    path('requestform/create/', views.FormCreateView.as_view(), name='form_create'),
    path('requestform/<int:pk>/update/', views.FormUpdateView.as_view(), name='form_update'),
    path('requestform/<int:pk>/delete/', views.FormDeleteView.as_view(), name='form_delete'),
]

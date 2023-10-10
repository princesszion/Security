# admin_requests/urls.py
from django.urls import path
from . import views

from django.urls import path
from .views import  RegisterUserAPIView, UserLoginView, AdminRequestListCreateView, AdminRequestDetailView
from . import views

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/',RegisterUserAPIView.as_view(), name='register-user'),
    path('admin-requests/',AdminRequestListCreateView.as_view(), name='admin-request-list-create'),
    path('admin-request/<int:pk>/', AdminRequestDetailView.as_view(), name='admin-request-detail'),
    path('student/<int:student_id>/', views.StudentDetailView.as_view(), name='student_detail'),

]

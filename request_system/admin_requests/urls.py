# admin_requests/urls.py
from django.urls import path
from . import views

from django.urls import path
from .views import  RegisterUserAPIView, UserLoginView, AdminRequestListCreateView, AdminRequestDetailView, StudentRequestsListView, StudentRepliesListView
from . import views

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/',RegisterUserAPIView.as_view(), name='register-user'),
    path('admin-requests/',AdminRequestListCreateView.as_view(), name='admin-request-list-create'),
    path('admin-request/<int:pk>/', AdminRequestDetailView.as_view(), name='admin-request-detail'),
    # List requests sent by the student
    path('student_requests/', StudentRequestsListView.as_view(), name='student-requests-list'),

    # List replies received by the student
    path('student_replies/', StudentRepliesListView.as_view(), name='student-replies-list'),
    path('', views.home, name='home'),
]

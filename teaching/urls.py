from django.urls import path

from . import views

urlpatterns = [
    path('teacher/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
]

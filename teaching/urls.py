from django.urls import path

from . import views

urlpatterns = [
    path('<str:university>/profesores/<str:teacher_nick>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
]

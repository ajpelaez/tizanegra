from django.urls import path

from . import views

urlpatterns = [
    path('<str:university>/<str:teacher>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
    path('<str:university>/<str:degree>/<str:subject>/', views.SubjectDetailView.as_view(), name='subject-detail'),
]

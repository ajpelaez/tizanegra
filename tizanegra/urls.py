from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('django.contrib.auth.urls')),

    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('user/panel/', views.UserPanelView.as_view(), name='panel'),
    path('user/check-username/<str:username>/', views.check_username_is_valid, name='check_username'),
    path('user/check-email/<str:email>/', views.check_email_is_valid, name='check_email'),

    path('api/get-teachers-and-subjects/<str:name>/', views.get_teachers_and_subjects,
         name='get_teachers_and_subjects'),
    path('api/report-comment/', views.report_comment, name='report_comment'),
    path('api/rate-comment/', views.rate_comment, name='rate_comment'),

    path('<str:university>/<str:teacher>/', views.TeacherDetailView.as_view(), name='teacher-detail'),
    path('<str:university>/<str:degree>/<str:subject>/', views.SubjectDetailView.as_view(), name='subject-detail'),

    path('', views.index, name='index'),
]


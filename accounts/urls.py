from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.UserCreate.as_view(), name='signup'),
    path('check-username/<str:username>/', views.check_username_is_valid, name='check_username'),
]

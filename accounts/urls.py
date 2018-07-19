from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('signup', views.UserCreate.as_view(), name='signup'),
    path('test', views.hello_world),
]
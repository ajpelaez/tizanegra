from django.urls import path
from .views import Registro

urlpatterns = [
    path('register/', Registro.as_view(), name='registro'),
]

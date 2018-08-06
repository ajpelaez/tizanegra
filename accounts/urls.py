from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('panel/', views.UserPanelView.as_view(), name='panel'),
    path('check-username/<str:username>/', views.check_username_is_valid, name='check_username'),
    path('check-email/<str:email>/', views.check_email_is_valid, name='check_email'),
]

from django.urls import path
from django.views.generic import TemplateView
from .views import (
    UserPatientRegisterAPIView,
    UserLoginAPIView, 
    UserViewAPI, 
    UserLogoutViewAPI, 
    PasswordResetRequestAPIView, 
    PasswordResetConfirmAPIView,
    ChangePasswordView
)

urlpatterns = [
    path('register/client', UserPatientRegisterAPIView.as_view(), name='register.client'),
    #path('register/worker', UserRegistrationAPIView.as_view(), name='register.worker'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('profile/', UserViewAPI.as_view(), name="profile"),
	path('logout/', UserLogoutViewAPI.as_view(), name="logout"),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('reset-password-confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    ##path('reset-password/<uidb64>/<token>/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
    ##path('password-reset/complete/', TemplateView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    ##path('password-reset/invalid/', TemplateView.as_view(template_name='password_reset_invalid.html'), name='password_reset_invalid'),
]
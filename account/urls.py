from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='user_register'),
    path('verify/',views.UserRegisterVerifyCodeView.as_view(),name='verify_code'),
    path('Login/',views.UserLoginView.as_view(),name='User_Login'),
    path('Logout/',views.UserLogoutView.as_view(),name='User_Logout'),
    path('Login-Verify/',views.UserLoginVerifyCodeView.as_view(),name='verify_code_login'),
]
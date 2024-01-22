"""
URL configuration для приложения users.
"""

from django.urls import path

from users import views
from users.apps import UsersConfig
from users.views import UserRegisterView, UserProfileView, LoginView, VerificationTemplateView, generate_new_password

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('verify_email', VerificationTemplateView.as_view(), name='verify_email'),
    path('profile/genpassword', generate_new_password, name='generate_new_password'),
]

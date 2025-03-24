from django.urls import path
from .views import (
    RegistUserView, LoginView, LogoutView, UserUpdateView
)

app_name = 'accounts'
urlpatterns = [
    path('regist/', RegistUserView.as_view(template_name='accounts/regist.html'), name='regist'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='accounts/logout'),
    path('user_edit/<int:pk>/', UserUpdateView.as_view(template_name='accounts/user_update.html'), name='user_edit')
]

from django.urls import path
from .views import (
    RegistUserView, LoginView, LogoutView,
    UserUpdateView, PasswordChangeView,
    MyPageView, invite_family, generate_invite_url,
)

app_name = 'accounts'
urlpatterns = [
    path('regist/', RegistUserView.as_view(template_name='accounts/regist.html'), name='regist'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='accounts/logout'),
    path('user_edit/<int:pk>/', UserUpdateView.as_view(template_name='accounts/user_update.html'), name='user_edit'),
    path('password_change/', PasswordChangeView.as_view(template_name = 'accounts/password_change.html'), name='password_change'),
    path('mypage/', MyPageView.as_view(template_name='accounts/mypage.html'), name='mypage'),
    path('invite_family/', invite_family, name='invite_family'),
    path('generate_invite_url/', generate_invite_url, name='generate_invite_url'),
]



from django.urls import path
from .views import (
    RegistUserView, LoginView, LogoutView,
    UserUpdateView, PasswordChangeView,
)
from . import views
app_name = 'accounts'
urlpatterns = [
    path('regist/', RegistUserView.as_view(template_name='accounts/regist.html'), name='regist'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='accounts/logout'),
    path('user_edit/<int:pk>/', UserUpdateView.as_view(template_name='accounts/user_update.html'), name='user_edit'),
    path('password_change/', PasswordChangeView.as_view(template_name = 'accounts/password_change.html'), name='password_change'),
    path('my_page/', views.my_page, name='mypage'),
    path('invite_family/', views.invite_family, name='invite_family'),
    path('remove_family_member/<int:family_id>/<int:user_id>/', views.remove_family_member, name='remove_family_member'),
    path('add_child/', views.add_child, name='add_child'),
]



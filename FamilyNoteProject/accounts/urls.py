from django.urls import path
from .views import (
    RegistUserView, LoginView, LogoutView
)

app_name = 'accounts'
urlpatterns = [
    path('regist/', RegistUserView.as_view(template_name='accounts/regist.html'), name='regist'),
    path('login/',LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='accounts/logout'),
]

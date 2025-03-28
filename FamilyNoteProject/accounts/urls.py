from django.urls import path






# from django.urls import path
# from .views import (
#     RegistUserView, LoginView, LogoutView,
#     UserUpdateView, PasswordChangeView, MyPageView,
#     invite_family_view, generate_invite, JoinFamilyView,
# )
# from . import views
# app_name = 'accounts'
# urlpatterns = [
#     path('regist/', RegistUserView.as_view(template_name='accounts/regist.html'), name='regist'),
#     path('login/',LoginView.as_view(template_name='accounts/login.html'), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('user_edit/<int:pk>/', UserUpdateView.as_view(template_name='accounts/user_update.html'), name='user_edit'),
#     path('password_change/', PasswordChangeView.as_view(template_name = 'accounts/password_change.html'), name='password_change'),
#     path('my_page/', MyPageView.as_view(template_name='accounts/my_page.html'), name='my_page'),
#     path('invite/', invite_family_view, name='invite_family'),
#     path('invite/', generate_invite, name='generate_invite'),
#     path('join/<uuid:invite_code>/', JoinFamilyView.as_view(template_name = 'accounts/family_regist.html'), name='join_family'),
#     path('remove_family_member/<int:family_id>/<int:user_id>/', views.remove_family_member, name='remove_family_member'),
#     path('add_child/', views.add_child, name='add_child'),
# ]



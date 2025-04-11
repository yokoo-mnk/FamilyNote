from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path("register/", views.register, name="register"),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("mypage/", views.mypage, name="mypage"),
    path("user_edit/<int:pk>/", views.UserUpdateView.as_view(), name="user_edit"),
    path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path("add_child/", views.add_child, name="add_child"),
    path('get_child_data/<int:child_id>/', views.get_child_data, name='get_child_data'),
    path("edit_child/<int:child_id>/", views.edit_child, name="edit_child"),
    path("delete_child/<int:child_id>/", views.delete_child, name="delete_child"),
]
from django.urls import path
from . import views 

app_name = 'families'

urlpatterns = [
    path("create_family/", views.create_family, name="create_family"),
    path("invite/", views.invite_family, name="invite_family"),
    path("join/<uuid:invite_code>/", views.join_family, name="join_family"),
    path('invite/<invite_code>/', views.invite_register_redirect, name='invite-register'),
    path("leave/", views.leave_family, name="leave_family"),
]

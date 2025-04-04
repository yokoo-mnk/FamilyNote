from django.urls import path
from . import views 

app_name = 'families'

urlpatterns = [
    path("create_family/", views.create_family, name="create_family"),
    path("invite/", views.invite_family, name="invite_family"),
    path("join/<uuid:invite_code>/", views.join_family, name="join_family"),
    path("leave/", views.leave_family, name="leave_family"),
    path("leave/", views.confirm_leave_family, name="confirm_leave_family"),
]

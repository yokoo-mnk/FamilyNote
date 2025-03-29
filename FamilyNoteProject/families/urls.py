from django.urls import path
from .views import (
    create_family, invite_family, join_family, leave_family,
    confirm_leave_family,
)
app_name = 'families'

urlpatterns = [
    path("family/create/", create_family, name="create_family"),
    path("invite/", invite_family, name="invite_family"),
    path("join/<uuid:invite_code>/", join_family, name="join_family"),
    path("leave/", leave_family, name="leave_family"),
    path("leave/", confirm_leave_family, name="confirm_leave_family"),
]

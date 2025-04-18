from django.urls import path
from . import views

app_name = 'school_letters'

urlpatterns = [
    path('create_letter/', views.SchoolLetterCreateView.as_view(), name='create_letter'),
    path('update_letter/<int:pk>/', views.SchoolLetterUpdateView.as_view(), name='update_letter'),
    path('letter_list/', views.SchoolLetterListView.as_view(), name='letter_list'),
    path("delete_letter/", views.SchoolLetterDeleteView.as_view(), name="delete_letters"),
]
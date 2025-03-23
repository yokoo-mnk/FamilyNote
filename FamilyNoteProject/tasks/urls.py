from django.urls import path

app_name = 'tasks'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
]
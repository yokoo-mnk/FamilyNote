from django.urls import path
from .views import (
    home, TaskListView, TaskCreateView, TaskUpdateView,
)

app_name = 'tasks'
urlpatterns = [
    path('home/', home, name='home'),
    path('task_list/', TaskListView.as_view(template_name='tasks/task_list.html'), name='task_list'),
    path('task_create/', TaskCreateView.as_view(template_name='tasks/task_create.html'), name='task_create'),
    path('task_edit/<int:pk>/', TaskUpdateView.as_view(template_name='tasks/task_update.html'), name='task_edit')
]
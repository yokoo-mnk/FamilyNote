from django.urls import path
from .views import (
    TaskListView, TaskCreateView,
)

app_name = 'tasks'
urlpatterns = [
    path('task_list/', TaskListView.as_view(template_name='tasks/task_list.html'), name='task_list'),
    path('task_create/', TaskCreateView.as_view(template_name='tasks/task_create.html'), name='task_create'),
]
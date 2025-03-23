from django.urls import path
from .views import (
    TaskListView,
)

app_name = 'tasks'
urlpatterns = [
    path('tasks/', TaskListView.as_view(template_name='tasks/task_list.html'), name='task_list'),
]
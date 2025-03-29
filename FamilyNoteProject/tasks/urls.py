from django.urls import path
from . import views
from .views import (
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    TaskCopyView,
)

app_name = 'tasks'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('task_list/', TaskListView.as_view(template_name='tasks/task_list.html'), name='task_list'),
    path('task_create/', TaskCreateView.as_view(template_name='tasks/task_create.html'), name='task_create'),
    path('task_edit/<int:pk>/', TaskUpdateView.as_view(template_name='tasks/task_update.html'), name='task_edit'),
    path('task_delete/<int:pk>/', TaskDeleteView.as_view(template_name='tasks/task_delete.html'), name='task_delete'),
    path("<int:task_id>/copy/", TaskCopyView.as_view(), name="task_copy"),
]
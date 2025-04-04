from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('task_list/', views.TaskListView.as_view(template_name='tasks/task_list.html'), name='task_list'),
    path('task_create/', views.TaskCreateView.as_view(template_name='tasks/task_create.html'), name='task_create'),
    path('task_edit/<int:pk>/', views.TaskUpdateView.as_view(template_name='tasks/task_update.html'), name='task_edit'),
    path('task_delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path("<int:task_id>/copy/", views.TaskCopyView.as_view(), name="task_copy"),
]
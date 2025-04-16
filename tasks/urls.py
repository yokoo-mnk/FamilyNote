from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('home/', views.HomeTaskListView.as_view(), name='home'),
    path('home_task_remove/', views.HomeTaskRemoveView.as_view(), name='home_task_remove'),
    path('toggle_completion/', views.toggle_task_completion, name='toggle_completion'),
    path('assign_task_member/', views.assign_task_member, name='assign_task_member'),
    path('task_list/', views.TaskListView.as_view(), name='task_list'),
    path('task_create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task_edit/<int:pk>/', views.TaskUpdateView.as_view(), name='task_edit'),
    path('task_delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('task/<int:task_id>/copy/confirm/', views.TaskCopyConfirmView.as_view(), name='task_copy_confirm'),
    path('task/<int:task_id>/copy/execute/', views.TaskCopyExecuteView.as_view(), name='task_copy_execute'), 
]
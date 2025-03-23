from django.shortcuts import render
from django.views.generic import ListView
from .models import Task

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'  # 使用するテンプレートのファイル名
    context_object_name = 'tasks'  # テンプレートで利用するコンテキスト変数名
    paginate_by = 10 
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
)
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('task_list')
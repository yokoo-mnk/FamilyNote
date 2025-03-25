from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
from .models import Task
from .forms import TaskForm
from django.urls import reverse_lazy

class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        for task in context['tasks']:
            task.formatted_due_date = task.due_date.strftime('%m/%d')
        return context

class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_create.html'
    success_url = reverse_lazy('tasks:task_list')
    
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_update.html'
    success_url = reverse_lazy('tasks:task_list')
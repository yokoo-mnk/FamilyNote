from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, View,
)
from .models import Task
from .forms import TaskForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


@login_required
def home(request):
    return render(request, 'tasks/home.html')


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        return Task.objects.filter(family=self.request.user.family)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for task in context['tasks']:
            task.formatted_due_date = task.due_date.strftime('%m/%d')
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def form_valid(self, form):
        form.instance.family = self.request.user.family
        return super().form_valid(form)
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks:task_list')
    
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("tasks/task_list")
    
class TaskCopyView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        
        new_task = Task.objects.create(
            family=task.family,
            title=f"{task.title} (コピー)",
            description=task.description,
            assigned_to=task.assigned_to,
            due_date=task.due_date
        )

        return HttpResponseRedirect(reverse("task_list"))
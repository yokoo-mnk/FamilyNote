from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, View,
)
from django.db.models import Q
from .models import Task, Family
from .forms import TaskForm
from django.urls import reverse, reverse_lazy


class HomeTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/home.html'
    context_object_name = 'home_tasks'

    def get_queryset(self):
        return Task.objects.filter(
            family=self.request.user.family,
            show_on_home=True
        ).order_by('due_date')
        

class HomeTaskRemoveView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, family=request.user.family)
        task.show_on_home = False
        task.save()
        return redirect('tasks:home')

        
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Task.objects.filter(family=self.request.user.family)
        category = self.request.GET.get("category")
        search_query = self.request.GET.get("search")
        
        if category:
            queryset = queryset.filter(category=category)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(memo__icontains=search_query)
            )
            
        if self.request.GET.get('is_favorite') == 'on':  # チェックボックスがオンの場合
            queryset = queryset.filter(is_favorite=True)
            
        return queryset   
    
    def post(self, request, *args, **kwargs):
        task_ids = request.POST.getlist('tasks')
        action = request.POST.get('action')
        
        if not task_ids:
            return redirect("tasks:task_list")
        
        tasks = Task.objects.filter(id__in=task_ids, family=request.user.family)

        if action == 'delete':
            tasks.delete()

        elif action == 'show_on_home':
            tasks.update(show_on_home=True)

        return redirect("tasks:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["categories"] = Task.CATEGORY_CHOICES
        context["selected_category"] = self.request.GET.get("category", "")
        context["search_query"] = self.request.GET.get("search", "")
        context["is_favorite_filter"] = self.request.GET.get('is_favorite', '')
        
        for task in context['tasks']:
            task.formatted_due_date = task.due_date.strftime('%m/%d')
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def form_valid(self, form):
        family = Family.objects.filter(members=self.request.user).first()
        
        if not family:
            messages.error(self.request, "先に Family を作成してください。")
            return redirect("accounts:mypage")
        
        form.instance.family = family
        
        form.instance.is_favorite = self.request.POST.get('is_favorite') == 'on'
        form.instance.show_on_home = self.request.POST.get('show_on_home') == 'on'

        return super().form_valid(form)
    
    def get_initial(self):
        """ クエリパラメータから初期値を取得 """
        initial = super().get_initial()
        initial["title"] = self.request.GET.get("title", "")
        initial["due_date"] = self.request.GET.get("due_date", "")
        initial["start_time"] = self.request.GET.get("start_time", "")
        initial["memo"] = self.request.GET.get("memo", "")
        initial["category"] = self.request.GET.get("category", "")
        initial["is_favorite"] = self.request.GET.get("is_favorite", "") == "on"
        initial["show_on_home"] = self.request.GET.get("show_on_home", "") == "on"
        return initial
    
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def form_valid(self, form):
        form.instance.is_favorite = self.request.POST.get('is_favorite') == 'on'
        form.instance.show_on_home = self.request.POST.get('show_on_home') == 'on'
        return super().form_valid(form)
    
    
class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task_ids = request.POST.getlist("tasks")
        if task_ids:
            Task.objects.filter(id__in=task_ids, family=request.user.family).delete()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "削除するタスクが選択されていません。"})
    
    
class TaskCopyView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        
        query_params = {
            "title": task.title,
            "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
            "start_time": task.start_time.strftime("%H:%M") if task.start_time else "",
            "memo": task.memo,
            "category": task.category,
            "is_favorite": "on" if task.is_favorite else "",
            "show_on_home": "on" if task.show_on_home else "",
        }
        
        url = reverse("tasks:task_create") + "?" + "&".join(
            [f"{key}={value}" for key, value in query_params.items() if value])
        return redirect(url)
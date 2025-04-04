from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, CreateView, UpdateView, View,
)
from django.db.models import Q
from .models import Task, Family
from .forms import TaskForm
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect


@login_required
def home(request):
    selected_task_ids = request.session.get('selected_tasks', [])
    selected_tasks = Task.objects.filter(id__in=selected_task_ids)
    
    if request.method == 'POST' and 'remove_task' in request.POST:
        task_ids_to_remove = request.POST.getlist('remove_task')
        selected_task_ids = [task_id for task_id in selected_task_ids if task_id not in task_ids_to_remove]
        request.session['selected_tasks'] = selected_task_ids
        return redirect('tasks:home')
    return render(request, 'tasks/home.html', {'selected_tasks': selected_tasks})


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
            # title と memo に対して検索
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(memo__icontains=search_query)
            )
            
        if self.request.GET.get('is_favorite') == 'on':  # チェックボックスがオンの場合
            queryset = queryset.filter(is_favorite=True)
            
        return queryset   
    
    def post(self, request, *args, **kwargs):
        task_ids = request.POST.getlist('tasks')
        selected_tasks = request.session.get('selected_tasks', [])
        selected_tasks.extend(task_ids)
        request.session['selected_tasks'] = selected_tasks
        return HttpResponseRedirect(request.path)
    
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
        
        is_favorite = self.request.POST.get('is_favorite')
        form.instance.is_favorite = is_favorite == 'on'
        return super().form_valid(form)
    
    def get_initial(self):
        """ クエリパラメータから初期値を取得 """
        initial = super().get_initial()
        initial["title"] = self.request.GET.get("title", "")
        initial["due_date"] = self.request.GET.get("due_date", "")
        initial["start_time"] = self.request.GET.get("start_time", "")
        initial["memo"] = self.request.GET.get("memo", "")
        initial["category"] = self.request.GET.get("category", "")
        initial["is_favorite"] = self.request.GET.get("is_favorite", "")
        return initial
    
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def form_valid(self, form):
        # お気に入り状態の更新
        is_favorite = self.request.POST.get('is_favorite')
        form.instance.is_favorite = is_favorite == 'on'
        
        return super().form_valid(form)
    
    
class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task_ids = request.POST.getlist("tasks")
        if task_ids:
            Task.objects.filter(id__in=task_ids, family=request.user.family).delete()
        return redirect("tasks:task_list")
    
    
class TaskCopyView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        
        query_params = {
            "title": task.title,
            "due_date": task.due_date.strftime("%Y-%m-%d") if task.due_date else "",
            "start_time": task.start_time.strftime("%H:%M") if task.start_time else "",
            "memo": task.memo,
            "category": task.category,
            "is_favorite": task.is_favorite,
        }
        
        url = reverse("tasks:task_create") + "?" + "&".join([f"{key}={value}" for key, value in query_params.items() if value])
        return redirect(url)
from django.http import JsonResponse
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView, CreateView, UpdateView, View,
)
from django.db.models import Q
from .models import Task, Family
from .forms import TaskForm
from django.urls import reverse, reverse_lazy
from datetime import date
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import os

User = get_user_model()

class HomeTaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/home.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Task.objects.filter(
            family=self.request.user.family,
            show_on_home=True
        )

        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)
        
        assignee_id = self.request.GET.get("assignee")
        if assignee_id == "all":
            queryset = queryset.filter(assigned_to__isnull=True, is_all_assigned=True)
        elif assignee_id:
            queryset = queryset.filter(assigned_to__id=assignee_id)
        
        sort_order = self.request.GET.get('sort_order', 'oldest')
        
        if sort_order == 'newest':
            queryset = queryset.order_by('-due_date', '-start_time')
        elif sort_order == 'oldest':
            queryset = queryset.order_by('due_date', 'start_time')
        else:
            queryset = queryset.order_by('due_date', 'start_time')
        
        for task in queryset:
            if task.due_date:
                task.is_today = task.due_date == date.today()
                task.is_overdue = task.due_date < date.today()
                task.formatted_due_date = task.due_date.strftime('%y/%m/%d')
            else:
                task.is_today = False
                task.is_overdue = False
                task.formatted_due_date = ""
        
            if task.assigned_to is None:
                if task.is_all_assigned:
                    task.assigned_to_id_str = "all"
                else:
                    task.assigned_to_id_str = ""
            else:
                task.assigned_to_id_str = str(task.assigned_to.id)
        
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["selected_category"] = self.request.GET.get("category", "")
        context["categories"] = Task.CATEGORY_CHOICES
        
        assignee_param = self.request.GET.get("assignee")
        context["selected_assignee"] = assignee_param if assignee_param is not None else ""
        
        context["selected_sort_order"] = self.request.GET.get('sort_order', 'oldest')
        context["today"] = date.today()
        
        family = self.request.user.family
        if family:
            context["family_members"] = family.members.all()
        else:
            context["family_members"] = []

        return context

class HomeTaskRemoveView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task_ids = request.POST.getlist("tasks")
        if task_ids:
            Task.objects.filter(
                id__in=task_ids, 
                family=request.user.family, 
                show_on_home=True
            ).update(show_on_home=False)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "削除するToDoが選択されていません。"})   


@require_POST
@login_required
def assign_task_member(request):
    try:
        data = json.loads(request.body)
        task_id = data.get("task_id")
        user_id = data.get("user_id")

        task = Task.objects.get(id=task_id)
        
        if user_id == "all":
            task.assigned_to = None
            task.is_all_assigned = True
        elif user_id:
            user = User.objects.get(id=user_id)

            if user.family != request.user.family:
                return JsonResponse({"success": False, "error": "権限がありません"})
            
            task.assigned_to = user
            task.is_all_assigned = False
        else:
            task.assigned_to = None
            task.is_all_assigned = False
            
        task.save()
        return JsonResponse({"success": True})
            
    except Task.DoesNotExist:
        return JsonResponse({"success": False, "error": "タスクが存在しません"})
    except User.DoesNotExist:
        return JsonResponse({"success": False, "error": "ユーザーが存在しません"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
          
            
@require_POST
@login_required
def toggle_task_completion(request):
   if request.method == "POST":
        task_id = request.POST.get("task_id")
        is_completed = request.POST.get("is_completed") == "true"

        try:
            task = Task.objects.get(id=task_id)
            task.is_completed = is_completed
            task.save()
            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"})


def toggle_show_on_home(request):
    if request.method == "POST":
        task_id = request.POST.get("task_id")
        show_on_home = request.POST.get("show_on_home") == "true"
        
        try:
            task = Task.objects.get(id=task_id)
            task.show_on_home = show_on_home
            task.save()
            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "タスクが見つかりません"})


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Task.objects.filter(family=self.request.user.family)
        category = self.request.GET.get("category")
        search_query = self.request.GET.get("search")
        is_favorite = self.request.GET.get("is_favorite")
        
        if category:
            queryset = queryset.filter(category=category)
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(memo__icontains=search_query)
            )
            
        if is_favorite == "only":
            queryset = queryset.filter(is_favorite=True)
            
        return queryset.order_by('-created_at')   
    
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
        context["selected_is_favorite"] = self.request.GET.get("is_favorite", "")
        
        for task in context['tasks']:
            task.formatted_due_date = task.due_date.strftime('%y/%m/%d')
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def form_valid(self, form):
        family = Family.objects.filter(members=self.request.user).first()
        
        if not family:
            messages.error(self.request, "先に下記の家族を作成するリンクから<br>家族の名前を登録してください。")
            return redirect("accounts:mypage")
        
        form.instance.family = family
        
        form.instance.is_favorite = self.request.POST.get('is_favorite') == 'on'
        form.instance.show_on_home = self.request.POST.get('show_on_home') == 'on'

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.__class__.__name__
        return context
    
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
        
        assignee_id = self.request.POST.get('assigned_to')
        
        if assignee_id == "all" or not assignee_id:
            form.instance.assigned_to = None
        else:
            try:
                form.instance.assigned_to = User.objects.get(id=assignee_id)
            except User.DoesNotExist:
                form.add_error('assigned_to', "担当者が見つかりません")
                return self.form_invalid(form)
        
        return super().form_valid(form)
    
    
class TaskDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task_ids = request.POST.getlist("tasks")
        if task_ids:
            Task.objects.filter(id__in=task_ids, family=request.user.family).delete()
            return JsonResponse({"success": True})
        return JsonResponse({"success": False, "error": "削除するタスクが選択されていません。"})
    
    
class TaskCopyExecuteView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        original_task = get_object_or_404(Task, id=task_id)

        copied_task = Task.objects.create(
            family=request.user.family,
            title=original_task.title,
            due_date=original_task.due_date,
            start_time=original_task.start_time,
            memo=original_task.memo,
            category=original_task.category,
            is_favorite=original_task.is_favorite,
            show_on_home=original_task.show_on_home,
        )
        
        if original_task.image:
            image_file = original_task.image
            image_file.open()
            copied_task.image.save(
                os.path.basename(image_file.name),
                ContentFile(image_file.read()),
                save=True
            )
            image_file.close()

        return redirect("tasks:task_edit", pk=copied_task.pk)
    
    
class TaskCopyConfirmView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'tasks/task_copy_confirm.html', {"task": task})
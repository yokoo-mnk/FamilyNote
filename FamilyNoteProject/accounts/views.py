from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import UpdateView
from .models import  CustomUser, Child
from .forms import (
    CustomUserCreationForm, CustomLoginForm, UserUpdateForm,
)
from django.contrib.auth.views import(
    LoginView, LogoutView, PasswordChangeView,
)
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, get_user_model
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get('next', 'tasks:home')
            return redirect(next_url)

    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy('tasks:home')

    
class CustomLogoutView(LogoutView):
    next_page = "accounts/accounts/login"


@login_required
def mypage(request):
    user = request.user
    family_members = CustomUser.objects.filter(family=user.family) if user.family else []
    children = Child.objects.filter(family=user.family) if user.family else []
   
    context = {
        "user": user,
        "family_members": family_members,
        "children": children,
    }
    return render(request, "accounts/mypage.html", context)


@login_required
def add_child(request):
    if request.method == "POST":
        child_name = request.POST.get('child_name')
        birth_date_str = request.POST.get('birth_date')
        if not child_name or not birth_date_str:
            return JsonResponse({
                "success": False,
                "errors": "名前と生年月日が必要です"
            }, status=400)
            
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            return JsonResponse({
                "success": False,
                "errors": "日付の形式が正しくありません"
            }, status=400)
        
        child = Child(
            child_name=child_name,
            birth_date=birth_date,
            family=request.user.family,
        )
        child.save()
        
        return JsonResponse({
            "success": True,
            "child_name": child_name, 
            "birth_date": birth_date.strftime("%Y-%m-%d")
        })
        
    return JsonResponse({"success": False, "errors": "Invalid request method"})


@login_required
def get_child_data(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    return JsonResponse({
        'success': True,
        'child': {
            'id': child.id,
            'child_name': child.child_name,
            'birth_date': child.birth_date,
        }
    })


@login_required
@csrf_exempt
def edit_child(request, child_id):
    if request.method == 'POST':
        child_id = request.POST.get('child_id')
        child_name = request.POST.get('child_name')
        birth_date = request.POST.get('birth_date')
        
        child = get_object_or_404(Child, id=child_id)
        child.child_name = child_name
        child.birth_date = birth_date
        child.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'POST method required'})


@login_required
def delete_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)

    if request.user.family != child.family:
        return HttpResponseForbidden("削除権限がありません。")

    child.delete()
    return JsonResponse({"status": "deleted"})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/user_update.html"
    
    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])
    
    def get_success_url(self):
        return reverse_lazy("accounts:mypage")


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:my_page")
    
    def form_valid(self, form):
        messages.success(self.request, 'パスワードが正常に更新されました。')
        return super().form_valid(form)

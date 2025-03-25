from django.shortcuts import render, redirect
from django.views.generic import(
    TemplateView, FormView, View
)
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.urls import reverse_lazy
import uuid
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from .models import User
from .forms import RegistForm, LoginForm, UserUpdateForm

class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('tasks:task_list')#ホーム画面作ったらここに入れる（今は適当にtask一覧へ遷移）

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('tasks:task_list')#ホーム画面作ったらここに入れる（今は適当にtask一覧へ遷移）
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user:
            login(self.request, user)
        return super().form_valid(form)
    
class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('accounts:mypage')
    
    def get_object(self, queryset=None):
        return self.request.user
    

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "password_change.html"
    success_url = reverse_lazy("accounts:mypage")
    
 
class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "mypage.html"
    
@login_required
def invite_family(request):
    return render(request, "accounts/invite_family.html")

@login_required
def generate_invite_url(request):
    invite_url = f"https://example.com/invite/{uuid.uuid4()}/"
    return JsonResponse({"invite_url": invite_url})
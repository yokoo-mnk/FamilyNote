from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import UpdateView, FormView
from .models import  CustomUser, Child
from .forms import (
    CustomUserCreationForm, CustomLoginForm, UserUpdateForm,
)
from django.contrib.auth.views import(
    LoginView, LogoutView,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomPasswordChangeForm

User = get_user_model()



def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get('next')
            if not next_url:
                next_url = reverse('accounts:mypage')
            return redirect(next_url)
        
        messages.success(request, "アカウントが作成されました！<br>まずは、マイページで家族を作成してください。")
        return redirect(reverse('my_page'))
    
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = "accounts/login.html"
    success_url = reverse_lazy('tasks:home')

    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


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
    
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "※ アカウント情報の変更が完了しました！")
        return self.render_to_response(self.get_context_data(form=form))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_name'] = self.__class__.__name__
        return context
    

class CustomPasswordChangeView(LoginRequiredMixin, FormView):
    form_class = CustomPasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:mypage")
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = self.request.user
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.save()
        
        update_session_auth_hash(self.request, user)
        
        messages.success(self.request, 'パスワードが正常に更新されました。')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'パスワード変更に失敗しました。')
        return super().form_invalid(form)
    

# ポートフォリオページ
def portfolio(request):
    return render(request, 'accounts/portfolio.html', {
        'title': 'FamilyNote',
        'description': 'FamilyNoteは、仕事・育児・家事に忙しい共働き家庭のための、スケジュール・ToDo・記録の一元管理アプリです。\nこのアプリを使うことで、夫婦間の役割分担を明確にし、必要なToDoや子どもの予定を漏れなく管理できます。\n家庭の情報が分散せず、夫婦がリアルタイムで更新・確認できる仕組みを提供します。',
        'images': [
            'accounts/images/todolist-image.png',
            'accounts/images/note-image.png',
            'accounts/images/schoolletter-image.png',
            'accounts/images/mypage-image.png',
        ],
        'documents': [
            {'name': '企画書', 'path': '/media/portfolio_docs/FamilyNote-企画書.pdf'},
            {'name': '画面設計図', 'path': '/media/portfolio_docs/FamilyNote-画面設計図.pdf'},
            {'name': '画面遷移図', 'path': '/media/portfolio_docs/FamilyNote-画面遷移図.svg'},
            {'name': 'ER図', 'path': '/media/portfolio_docs/FamilyNote-ER図.svg'},
        ],
        'login_link': '/accounts/accounts/login/',
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseForbidden
from django.views.generic import UpdateView
from .models import Child
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

User = get_user_model()


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get('next', 'tasks:home')
            return redirect('tasks:home')

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
    family_members = user.families.all() if user.family else []
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
            parent=request.user,  # ユーザーに関連付け
            family=request.user.family,
        )
        child.save()
        
        return JsonResponse({
            "success": True,
            "child_name": child_name, 
            "birth_date": birth_date.strftime("%Y-%m-%d")
        })
        
    return render(request, "accounts/add_child.html")


@login_required
def edit_child(request, child_id):
    child = get_object_or_404(Child, id=child_id)
    
    if request.user.family != child.family:
        return HttpResponseForbidden("この子供情報を編集する権限がありません。")
    
    if request.method == "POST":
        # フォームデータを取得
        child_name = request.POST.get('child_name')
        birth_date = request.POST.get('birth_date')
        
        if child_name and birth_date:
            # 子供の情報を更新
            child.child_name = child_name
            child.birth_date = birth_date
            child.save()
            
            return JsonResponse({
                "status": "success",
                "child_name": child.child_name,
                "birth_date": child.birth_date.strftime("%Y-%m-%d")
            })
        else:
            return JsonResponse({
                "status": "error",
                "message": "名前と生年月日は必須です。"
            }, status=400)
            
    return render(request, "accounts/edit_child_modal.html", {"child": child})


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



# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.generic import(
#     FormView, View, DetailView,
# )
# from django.views.generic.edit import (
#     CreateView, UpdateView,
# )
# from django.urls import reverse_lazy
# from django.http import JsonResponse
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.views import PasswordChangeView
# from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
# from .models import (
#     User, Family, FamilyInvitation,
# )
# from .forms import (
#     RegistForm, UserUpdateForm, ChildForm,
#     UserProfileForm
# )


# class RegistUserView(CreateView):#URL関係なしの一般的なアカウント登録
#     template_name = 'accounts/regist.html'
#     form_class = RegistForm
#     success_url = reverse_lazy('tasks:home')
    
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         user = self.object
        
#         login(self.request, user)
#         return response
    
       
# class LoginView(FormView):
#     template_name = 'accounts/login.html'
#     form_class = AuthenticationForm
#     success_url = reverse_lazy('tasks:home')
    
#     def form_valid(self, form):
#         email = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user = authenticate(self.request, email=email, password=password)
        
#         if user is not None:
#             login(self.request, user)
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)
        
#     def get_form_class(self):
#         form_class = super().get_form_class()
#         form_class.base_fields['username'].label = "メールアドレス"
#         return form_class
    
# class LogoutView(View):
#     def post(self, request, *args, **kwargs):
#         logout(request)
#         return redirect('accounts:login')
    
# class UserUpdateView(LoginRequiredMixin, UpdateView):#アカウント情報変更
#     model = User
#     form_class = UserUpdateForm
#     template_name = 'accounts/user_update.html'
#     success_url = reverse_lazy('accounts:user_update')
    
#     def get_object(self):
#         return self.request.user
    
#     def form_valid(self, form):
#         messages.success(self.request, 'アカウント情報が正常に更新されました。')
#         return super().form_valid(form)
    

# class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):#パスワード変更
#     form_class = PasswordChangeForm
#     template_name = "accounts/password_change.html"
#     success_url = reverse_lazy("accounts:my_page")
    
#     def form_valid(self, form):
#         messages.success(self.request, 'パスワードが正常に更新されました。')
#         return super().form_valid(form)
    

# @login_required
# def invite_family_view(request):#URL表示
#     return render(request, 'accounts/invite_family.html')


# @login_required
# def generate_invite(request):#URL発行
#     user = request.user
    
#     if not user.family:
#         return JsonResponse({'error': '家族に所属していません'}, status=400)
    
#     family = user.family
    
#     invitation = family.invitations.filter(is_used=False).first()
#     if not invitation:
#         invitation = FamilyInvitation.objects.create(family=family, inviter=user)
    
#     invite_url = request.build_absolute_uri(f"/accounts/join/{invitation.invite_code}/")

#     return JsonResponse({'invite_url': invite_url})


# class JoinFamilyView(CreateView):#URLからアカウント登録
#     template_name = 'accounts/family_regist.html'
#     form_class = RegistForm
#     success_url = reverse_lazy('tasks:home')

#     def dispatch(self, request, *args, **kwargs):
#         self.invite_code = kwargs.get('invite_code')
#         self.invitation = get_object_or_404(FamilyInvitation, invite_code=self.invite_code, is_used=False)
#         return super().dispatch(request, *args, **kwargs)
    
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         user = self.object
#         user.family = self.invitation.family
#         user.save()
        
#         self.invitation.is_used = True
#         self.invitation.save()
        
#         login(self.request, user)
#         return response
    

# class MyPageView(LoginRequiredMixin, DetailView):
#     model = User
#     template_name = 'accounts/my_page.html'
#     context_object_name = 'user'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['family'] = self.request.user.family
#         return context
    

# @login_required
# def remove_family_member(request, family_id, user_id):
#     family = get_object_or_404(Family, id=family_id)
#     user_to_remove = get_object_or_404(User, id=user_id)
    
#     if user_to_remove in family.members.all():
#         family.members.remove(user_to_remove)
#         messages.success(request, f'{user_to_remove.username} さんを家族から削除しました。')
#     else:
#         messages.error(request, '指定されたユーザーはこの家族のメンバーではありません。')
#     return redirect('accounts:my_page')    


# @login_required
# def add_child(request):
#     if request.method == 'POST':
#         form = ChildForm(request.POST)
#         if form.is_valid():
#             child = form.save(commit=False)
#             child.user = request.user
#             child.save()
#             return redirect('accounts:my_page')
#     else:
#         form = ChildForm()
    
#     return render(request, 'accounts:add_child.html', {'form': form})


# @login_required
# def update_profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('accounts:my_page')
#     else:
#         form = UserProfileForm(instance=request.user)

#     return render(request, 'accounts:update_profile.html', {'form': form})
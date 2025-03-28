from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

class CustomLogoutView(LogoutView):
    next_page = "login"








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
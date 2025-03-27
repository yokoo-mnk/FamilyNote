from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import(
    TemplateView, FormView, View
)
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.urls import reverse_lazy
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (
    authenticate, login, logout, get_user_model
)
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from .models import User, Family, Invitation
from .forms import (
    RegistForm, UserUpdateForm, ChildForm,
    UserProfileForm
)
from .decorators import family_required


class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm
    success_url = reverse_lazy('tasks:task_list')#ホーム画面作ったらここに入れる（今は適当にtask一覧へ遷移）
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        invite_url = self.request.GET.get("invite")
        
        if invite_url:
            try:
                family = Family.objects.get(invite_code=invite_url)
                family.members.add(user)
            except Family.DoesNotExist:
                pass 
            
        login(self.request, user)
        return response
    
       
class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('tasks:task_list')#ホーム画面作ったらここに入れる（今は適当にtask一覧へ遷移）
    
    def form_valid(self, form):
        email = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.base_fields['username'].label = "メールアドレス"
        return form_class
    
class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_update.html'
    success_url = reverse_lazy('accounts:user_update')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'アカウント情報が正常に更新されました。')
        return super().form_valid(form)
    

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:mypage")
    
    def form_valid(self, form):
        messages.success(self.request, 'パスワードが正常に更新されました。')
        return super().form_valid(form)
    
 
class MyPageView(LoginRequiredMixin, TemplateView):
    template_name = "mypage.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        families = user.families.all() if hasattr(user, 'families') else []
        
        context["families"] = families
        return context
    

@login_required
def create_invite(request):
    family = request.user.family
    if not family:
        return JsonResponse({"error": "You are not part of a family"}, status=400)
    
    invite = Invitation.objects.create(
        family=family,
        inviter=request.user,
        expires_at=now() + timedelta(days=1),
    )
    return JsonResponse({"invite_url": request.build_absolute_uri(invite.get_invite_url())})

@family_required
def invitation_url(request):
    family = request.user.family
    invite = Invitation.objects.create(
        family=family,
        inviter=request.user,
        expires_at=now() + timedelta(days=1),
    )
    invitation_link = request.build_absolute_uri(f"/invite/{invite.invite_id}/")

    return render(request, 'invite_family.html', {'invitation_link': invitation_link})


def accept_invite(request, invite_id):
    invite = get_object_or_404(Invitation, invite_id=invite_id, is_used=False)
    
    if invite.expires_at < now():
        return render(request, "invitation_expired.html")
    
    if request.user.is_authenticated:
        request.user.family = invite.family
        request.user.save()
        invite.is_used = True
        invite.save()
        return redirect("family_home")
    
    return render(request, "register.html", {"invite": invite})

@family_required
def family_home(request):
    return render(request, 'family_home.html')


@login_required
def remove_family_member(request, family_id, user_id):
    family = get_object_or_404(Family, id=family_id)
    user_to_remove = get_object_or_404(User, id=user_id)
    
    if user_to_remove in family.members.all():
        family.members.remove(user_to_remove)
        messages.success(request, f'{user_to_remove.username} さんを家族から削除しました。')
    else:
        messages.error(request, '指定されたユーザーはこの家族のメンバーではありません。')
    return redirect('accounts:mypage')    


@login_required
def add_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)
        if form.is_valid():
            child = form.save(commit=False)
            child.user = request.user
            child.save()
            return redirect('accounts:mypage')
    else:
        form = ChildForm()
    
    return render(request, 'add_child.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:mypage')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'update_profile.html', {'form': form})
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView, UpdateView, ListView
)
from django.views import View
from django.http import JsonResponse
from .models import SchoolLetter
from .forms import SchoolLetterForm
from accounts.models import Child


class SchoolLetterCreateView(LoginRequiredMixin, CreateView):
    model = SchoolLetter
    form_class = SchoolLetterForm
    template_name = 'school_letters/create_letter.html'
    success_url = reverse_lazy('school_letters:letter_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.family = self.request.user.family
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新しいおたより作成'
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SchoolLetterUpdateView(LoginRequiredMixin, UpdateView):
    model = SchoolLetter
    form_class = SchoolLetterForm
    template_name = 'school_letters/update_letter.html'
    success_url = reverse_lazy('school_letters:letter_list')
    
    def form_valid(self, form):
        # ユーザーが家族メンバーであることを確認
        if form.instance.family != self.request.user.family:
            return redirect('school_letters:list')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'おたより編集'
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
class SchoolLetterListView(LoginRequiredMixin, ListView):
    model = SchoolLetter
    template_name = 'school_letters/letter_list.html'
    context_object_name = 'letters'
    paginate_by = 8
    
    def get_queryset(self):
        family = self.request.user.family
        return SchoolLetter.objects.filter(family=family)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['children'] = Child.objects.filter(family=user.family)
        return context
    
    
class SchoolLetterDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        letter_ids = request.POST.getlist("delete_letter")
        
        deleted_count, _ = SchoolLetter.objects.filter(
            id__in=letter_ids
        ).delete()
        
        if deleted_count > 0:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "削除に失敗しました"})
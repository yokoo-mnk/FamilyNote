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
        form.instance.family = self.request.user.families.first()  # ユーザーの最初の家族を設定（例）
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '新しいおたより作成'
        return context


class SchoolLetterUpdateView(LoginRequiredMixin, UpdateView):
    model = SchoolLetter
    form_class = SchoolLetterForm
    template_name = 'school_letters/update_letter.html'
    success_url = reverse_lazy('school_letters:letter_list')
    
    def form_valid(self, form):
        # ユーザーが家族メンバーであることを確認
        if form.instance.family not in self.request.user.families.all():
            return redirect('school_letters:list')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'おたより編集'
        return context
    
class SchoolLetterListView(LoginRequiredMixin, ListView):
    model = SchoolLetter
    template_name = 'school_letters/letter_list.html'
    context_object_name = 'letters'
    # paginate_by = 4
    
    def get_queryset(self):
        family_ids = self.request.user.families.values_list('id', flat=True)
        return SchoolLetter.objects.filter(family__id__in=family_ids)
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     context['children'] = Child.objects.filter(family__in=user.families.all())  # 家族の子供一覧
    #     return context
    
class SchoolLetterDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        letter_ids = request.POST.getlist("delete_letter")
        # SchoolLetter.objects.filter(id__in=letter_ids, child__family__members=request.user).delete()
        # return JsonResponse({"success": True})
        deleted_count, _ = SchoolLetter.objects.filter(
            id__in=letter_ids, child__family__members=request.user
        ).delete()
        
        if deleted_count > 0:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "error": "削除に失敗しました"})
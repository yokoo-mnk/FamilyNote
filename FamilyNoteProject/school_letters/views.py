from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
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
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SchoolLetterUpdateView(LoginRequiredMixin, UpdateView):
    model = SchoolLetter
    form_class = SchoolLetterForm
    template_name = 'school_letters/update_letter.html'
    success_url = reverse_lazy('school_letters:letter_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
  
    
class SchoolLetterListView(LoginRequiredMixin, ListView):
    model = SchoolLetter
    template_name = 'school_letters/letter_list.html'
    context_object_name = 'letters'
    
    def get_queryset(self):
        user = self.request.user
        families = user.families.all()
        queryset = SchoolLetter.objects.filter(child__family__in=families).order_by('-id')
        
        child_id = self.request.GET.get('child_id')
        if child_id:
            queryset = queryset.filter(child_id=child_id)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['children'] = Child.objects.filter(family__in=user.families.all())  # 家族の子供一覧
        return context
    
class SchoolLetterDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        letter_ids = request.POST.getlist("delete_letter")
        SchoolLetter.objects.filter(id__in=letter_ids, child__family__members=request.user).delete()
        return JsonResponse({"success": True})
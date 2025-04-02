from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
from .models import SchoolLetter
from .forms import SchoolLetterForm
from families.models import Family

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
    template_name = 'school_letters/create_letter.html'
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
        return SchoolLetter.objects.filter(child__family__in=families)
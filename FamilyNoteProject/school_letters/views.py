from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
from .models import Letter
from django.urls import reverse_lazy

class LetterListView(LoginRequiredMixin, ListView):
    model = Letter
    template_name = 'letter_list.html'
    context_object_name = 'school_letters'
    

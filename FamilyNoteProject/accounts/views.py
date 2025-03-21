from django.shortcuts import render
from django.views.generic import(
    TemplateView, CreateView, FormView, View
)
from .forms import RegistForm, LoginForm

class HomeView(TemplateView):
    template_name = 'home.html'
    
class RegistUserView(CreateView):
    template_name = 'regist.html'
    form_class = RegistForm

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    
class LogoutView(View):
    pass
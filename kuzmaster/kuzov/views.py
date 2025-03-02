from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.views import View
from .forms import FormAuto
from .models import Auto, ZakazNaryad
from .utils import DataMixin


class KuzovHome(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/index.html'
    context_object_name = 'naryad'
    title_page = 'Главная страница'

    def get_queryset(self):
        return ZakazNaryad.objects.all()
    

class AddAuto(LoginRequiredMixin, CreateView):
    form_class = FormAuto
    template_name = 'kuzov/addauto.html'
    title_page = 'Добавление автомобиля'
  

#    def form_valid(self, form):
#        w = form.save(commit=False)
#        w.author = self.request.user
#        return super().form_valid(form)

def zakaz(request):
    pass

def avans(request):
    pass

def raskhod(request):
    pass
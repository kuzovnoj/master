from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.views import View
from .forms import FormAuto
from .models import Auto, ZakazNaryad

# Create your views here.

class KuzovHome(ListView):
    template_name = 'kuzov/index.html'
    context_object_name = 'naryad'
    extra_context = {'title': 'Главная'}

    def get_queryset(self):
        return ZakazNaryad.objects.all()
    


class AddAuto(CreateView):
    form_class = FormAuto
    template_name = 'kuzov/addauto.html'
    title_page = 'Добавление автомобиля'
  

#    def form_valid(self, form):
#        w = form.save(commit=False)
#        w.author = self.request.user
#        return super().form_valid(form)
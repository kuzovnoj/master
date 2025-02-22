from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.views import View
from forms import FormAuto

# Create your views here.

class KuzovHome(View):
    def get(self, request):
        return render(request, 'kuzov/index.html')
 
    def post(self, request):
        pass
    

class AddAuto(CreateView):
    form_class = FormAuto
    template_name = 'kuzov/addauto.html'
    title_page = 'Добавление автомобиля'
  

#    def form_valid(self, form):
#        w = form.save(commit=False)
#        w.author = self.request.user
#        return super().form_valid(form)
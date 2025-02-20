from django.shortcuts import render
from django.views.generic import ListView
from django.views import View

# Create your views here.

class KuzovHome(View):
    def get(self, request):
        return render(request, 'kuzov/index.html')
 
    def post(self, request):
        pass
    

    

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.views import View
from  . import forms
from .models import Auto, ZakazNaryad
from .utils import DataMixin
from django.urls import reverse_lazy


class KuzovHome(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/index.html'
    context_object_name = 'naryad'
    title_page = 'Главная страница'

    def get_queryset(self):
        return ZakazNaryad.objects.all()
    

class AddAuto(LoginRequiredMixin, CreateView):
    form_class = forms.FormAuto
    template_name = 'kuzov/addauto.html'
    title_page = 'Добавление автомобиля'
    

class AddClient(LoginRequiredMixin, CreateView):
    form_class = forms.FormClient
    template_name = 'kuzov/addclient.html'
    title_page = 'Добавление клиента'
    success_url = reverse_lazy('zakaz_naryad2')


class ZakazAddAuto(LoginRequiredMixin, CreateView):
    form_class = forms.FormAuto
    template_name = 'kuzov/addauto2.html'
    title_page = 'Новый заказ-наряд'
    success_url = reverse_lazy('client')


class ZakazNaryad2(LoginRequiredMixin, CreateView):
    form_class = forms.FormZakazNaryad
    template_name = 'kuzov/addauto2.html'
    title_page = 'Новый заказ-наряд'
    success_url = reverse_lazy('home')


class AddAvans(LoginRequiredMixin, CreateView):
    form_class = forms.FormAvans
    template_name = 'kuzov/addauto2.html'
    title_page = 'Взять аванс'
    success_url = reverse_lazy('home')

class AddOplata(LoginRequiredMixin, CreateView):
    form_class = forms.FormOplata
    template_name = 'kuzov/addauto2.html'
    title_page = 'Добавить оплату'
    success_url = reverse_lazy('home')

class AddRaskhod(LoginRequiredMixin, CreateView):
    form_class = forms.FormRaskhod
    template_name = 'kuzov/addauto2.html'
    title_page = 'Добавить расходник'
    success_url = reverse_lazy('home')
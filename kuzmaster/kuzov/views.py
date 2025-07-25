from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views import View
from django.http import HttpResponseNotFound
from  . import forms
from .models import Auto, ZakazNaryad, Client, Avans, Raskhod
from .utils import DataMixin
from django.urls import reverse_lazy
from django.db.models import Sum

class KuzovHome(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/index.html'
    context_object_name = 'naryad'
    title_page = 'Главная страница'

    def get_queryset(self):
        return ZakazNaryad.opened.all()

'''
class AddAuto(LoginRequiredMixin, CreateView):
    form_class = forms.FormAuto
    template_name = 'kuzov/addauto.html'
    title_page = 'Добавление автомобиля'
'''

class ZakazNaryad2(LoginRequiredMixin, CreateView):
    form_class = forms.FormZakazNaryad
    template_name = 'kuzov/addauto2.html'
    title_page = 'Новый заказ-наряд'
    success_url = reverse_lazy('home')

    def get_initial(self):
        initial = super(ZakazNaryad2, self).get_initial()
        pk_auto = int(self.kwargs['pk_slug'].split('_')[0])
        pk_client = int(self.kwargs['pk_slug'].split('_')[1])
        initial['auto'] = Auto.objects.get(pk=pk_auto)
        initial['client'] = Client.objects.get(pk=pk_client)
#        initial['master'] = get_user_model()
        return initial


def addclient_view(request, pk_auto):
    if request.method == 'POST':
        form = forms.FormClient(request.POST)
        if form.is_valid():
            w = Client.objects.create(**form.cleaned_data)
            if w.phone.startswith('8'):
                w.phone = '+7' + w.phone[1:]
                w.save()
            pk_client = w.pk
            pk_slug = str(pk_auto) + '_' + str(pk_client)
            return redirect('zakaz_naryad2', pk_slug)
    else:
        form = forms.FormClient()
    
    return render(request, 'kuzov/addclient.html', {'form': form})
    
'''
class AddClient(LoginRequiredMixin, CreateView):
    form_class = forms.FormClient
    template_name = 'kuzov/addclient.html'
    title_page = 'Добавление клиента'
    success_url = reverse_lazy('zakaz_naryad2')

    def form_valid(self, form):
        w = form.save(commit=False)
        if w.phone.startswith('8'):
            w.phone = '+7' + w.phone[1:]
        pk_slug = self.object.pk
        return super().form_valid(form)
'''

'''
class ZakazAddAuto(LoginRequiredMixin, CreateView):
    form_class = forms.FormAuto
    template_name = 'kuzov/addauto2.html'
    title_page = 'Новый заказ-наряд'
    success_url = reverse_lazy('client')
'''

def add_auto_view(request):
    if request.method == 'POST':
        form = forms.FormAuto(request.POST, request.FILES)
        if form.is_valid():
            w = Auto.objects.create(**form.cleaned_data)
            pk_auto = w.pk
            return redirect('client', pk_auto)
    else:
        form = forms.FormAuto()
    
    return render(request, 'kuzov/addauto2.html', {'form': form})


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


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')



class ShowOrder(DataMixin, DetailView):
    template_name = 'kuzov/order.html'
    slug_url_kwarg = 'order_id'
    context_object_name = 'order'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        return self.get_mixin_context(context, title=context['order'].auto)

    def get_object(self, queryset=None):
        return get_object_or_404(ZakazNaryad, pk=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['avans'] = Avans.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg]).aggregate(Sum('amount'))['amount__sum']
        context['raskhod'] = Raskhod.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg]).aggregate(Sum('amount'))['amount__sum']
        context['edit_url'] = 'edit_order'
        return context

class EditOrder(DataMixin, UpdateView):
    model = ZakazNaryad
    fields = ['remont', 'price']
    template_name = 'kuzov/addauto2.html'
    success_url = reverse_lazy('home')
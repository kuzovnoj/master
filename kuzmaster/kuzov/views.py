from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.views import View
from django.http import HttpResponseNotFound
from  . import forms
from .models import Auto, ZakazNaryad, Client, Avans, Raskhod, Oplata
from .utils import DataMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from .serializers import ZakazNaryadSerializer


class KuzovHome(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/index.html'
    context_object_name = 'naryad'
    title_page = 'Главная страница'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ZakazNaryad.opened.all()
        return ZakazNaryad.opened.filter(master__pk=self.request.user.pk)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            try:
                total = Oplata.objects.filter(cashier=self.request.user).aggregate(Sum('amount'))['amount__sum'] - \
                Avans.objects.filter(cashier=self.request.user).aggregate(Sum('amount'))['amount__sum'] - \
                Raskhod.objects.filter(cashier=self.request.user).aggregate(Sum('amount'))['amount__sum']
                context['total'] = total
            except:
                pass
        return context

class KuzovHomeDone(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/index.html'
    context_object_name = 'naryad'
    title_page = 'Выполненные'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return ZakazNaryad.done.all()
        return ZakazNaryad.done.filter(master__pk=self.request.user.pk)
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            try:
                total = Oplata.objects.filter(cashier=self.request.user).aggregate(Sum('amount'))['amount__sum'] - \
                Avans.objects.filter(cashier=self.request.user).aggregate(Sum('amount'))['amount__sum'] - \
                Raskhod.objects.filter(cashier=self.request.user).aggregate(Sum('amount'))['amount__sum']
                context['total'] = total
            except:
                pass
        return context

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
#        initial['master'] = self.request.user
        initial['client'] = Client.objects.get(pk=pk_client)
        return initial

@login_required
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
    
@login_required
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

@login_required
def last_operations_view(request):
    avans = Avans.objects.filter(cashier=request.user.pk).order_by('-time_create')[:10]
    raskhod = Raskhod.objects.filter(cashier=request.user.pk).order_by('-time_create')[:10]
    oplata = Oplata.objects.filter(cashier=request.user.pk).order_by('-time_create')[:10]

    data = {
        'title': 'Последние операции',
        'avans': avans,
        'raskhod': raskhod,
        'oplata': oplata,
    }

    return render(request, 'kuzov/last_operations.html', context=data)

class AddAvans(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = forms.FormAvans
    template_name = 'kuzov/addauto2.html'
    title_page = 'Взять аванс'
    success_url = reverse_lazy('home')
    permission_required = 'kuzov.add_avans'

    def get_initial(self):
        initial = super(AddAvans, self).get_initial()
        initial['cashier'] = self.request.user
        return initial


class AddOplata(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = forms.FormOplata
    template_name = 'kuzov/addauto2.html'
    title_page = 'Добавить оплату'
    success_url = reverse_lazy('home')
    permission_required = 'kuzov.add_oplata'
    
    def get_initial(self):
        initial = super(AddOplata, self).get_initial()
        initial['cashier'] = self.request.user
        return initial


class AddRaskhod(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = forms.FormRaskhod
    template_name = 'kuzov/addauto2.html'
    title_page = 'Добавить расходник'
    success_url = reverse_lazy('home')
    permission_required = 'kuzov.add_raskhod'

    def get_initial(self):
        initial = super(AddRaskhod, self).get_initial()
        initial['cashier'] = self.request.user
        return initial


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowOrder(DataMixin, DetailView):
    template_name = 'kuzov/order.html'
    slug_url_kwarg = 'order_id'
    context_object_name = 'order'

    def get_object(self, queryset=None):
        return get_object_or_404(ZakazNaryad, pk=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        sum_avans = Avans.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg]).aggregate(Sum('amount'))['amount__sum']
        sum_raskhod = Raskhod.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg], spare_part=False).aggregate(Sum('amount'))['amount__sum']
        sum_parts = Raskhod.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg], spare_part=True).aggregate(Sum('amount'))['amount__sum']
        sum_oplata = Oplata.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg]).aggregate(Sum('amount'))['amount__sum']
        if sum_avans:
            context['avans'] = sum_avans
        else:
            context['avans'] = 0
        if sum_raskhod:
            context['raskhod'] = sum_raskhod
        else:
            context['raskhod'] = 0
        if sum_parts:
            context['spare_part'] = sum_parts
        else:
            context['spare_part'] = 0
        if sum_oplata:
            context['oplata'] = sum_oplata
        else:
            context['oplata'] = 0
        context['to_be_paid'] = 'order.pk'
        context['edit_url'] = 'edit_order'
        context['title'] = 'Заказ-наряд ' + self.kwargs[self.slug_url_kwarg]
        return context


class EditOrder(DataMixin, UpdateView):
    model = ZakazNaryad
    fields = ['remont', 'price', 'in_work']
    template_name = 'kuzov/addauto2.html'
    success_url = reverse_lazy('home')


class EditAuto(DataMixin, UpdateView):
    model = Auto
    fields = ['marka', 'gos_num', 'photo']
    template_name = 'kuzov/addauto2.html'
    success_url = reverse_lazy('home')


class EditRaskhod(DataMixin, UpdateView):
    model = Raskhod
    fields = ['zakaz', 'amount', 'name', 'spare_part', 'date', 'cheque', 'cashier']
    template_name = 'kuzov/addauto2.html'
    success_url = reverse_lazy('home')

class EditAvans(DataMixin, UpdateView):
    model = Avans
    fields = ['zakaz', 'amount', 'comment', 'date']
    template_name = 'kuzov/addauto2.html'
    success_url = reverse_lazy('home')

class EditOplata(DataMixin, UpdateView):
    model = Oplata
    fields = ['zakaz', 'amount', 'date']
    template_name = 'kuzov/addauto2.html'
    success_url = reverse_lazy('home')

class OrderRaskhod(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/order_raskhod.html'
    context_object_name = 'order'
    title_page = 'Заказ-наряд расходник'
    slug_url_kwarg = 'order_id'

    def get_queryset(self):
        return Raskhod.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg], spare_part=False)
    

class OrderSparePart(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/order_spare_parts.html'
    context_object_name = 'order'
    title_page = 'Заказ-наряд запчасти'
    slug_url_kwarg = 'order_id'

    def get_queryset(self):
        return Raskhod.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg], spare_part=True)


class OrderAvans(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/order_avans.html'
    context_object_name = 'order'
    title_page = 'Заказ-наряд авансы'
    slug_url_kwarg = 'order_id'

    def get_queryset(self):
        return Avans.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg])


class OrderOplata(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'kuzov/order_oplata.html'
    context_object_name = 'order'
    title_page = 'Заказ-наряд оплата'
    slug_url_kwarg = 'order_id'

    def get_queryset(self):
        return Oplata.objects.filter(zakaz=self.kwargs[self.slug_url_kwarg])


class APIKuzovView(LoginRequiredMixin, ListModelMixin, GenericViewSet):
    queryset = ZakazNaryad.opened.all()
    serializer_class = ZakazNaryadSerializer
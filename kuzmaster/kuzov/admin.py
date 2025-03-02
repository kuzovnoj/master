from django.contrib import admin
from .models import Auto, ZakazNaryad, Client, Oplata, Avans, Raskhod
from django.db import models
from django.db.models import Count, Sum, Avg, Max, Min


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'marka', 'gos_num', 'time_create')
    list_editable = ('marka', 'gos_num')
    list_per_page = 12


@admin.register(ZakazNaryad)
class ZakazNaryadAdmin(admin.ModelAdmin):
    list_display = ('id', 'auto', 'master', 'client', 'remont', 'price', 'oplata',
                    'avans', 'raskhod', 'time_create', 'time_update')
    list_editable = ('master', 'remont', 'price')
    list_per_page = 12

    def oplata(self, zakaznaryad: ZakazNaryad):
        z1 = ZakazNaryad.objects.filter(oplata__zakaz=zakaznaryad.id).aggregate(Sum('oplata__amount'))
        return z1['oplata__amount__sum']
    
    def avans(self, zakaznaryad: ZakazNaryad):
        z1 = ZakazNaryad.objects.filter(avans__zakaz=zakaznaryad.id).aggregate(Sum('avans__amount'))
        return z1['avans__amount__sum']
    
    def raskhod(self, zakaznaryad: ZakazNaryad):
        z1 = ZakazNaryad.objects.filter(raskhod__zakaz=zakaznaryad.id).aggregate(Sum('raskhod__amount'))
        return z1['raskhod__amount__sum']

@admin.register(Client)
class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone')
    list_editable = ('name', 'phone')
    list_per_page = 12

@admin.register(Oplata)
class OplataAdmin(admin.ModelAdmin):
    list_display = ('id', 'zakaz', 'amount', 'time_create')
    list_editable = ('zakaz', 'amount')
    list_per_page = 12


@admin.register(Avans)
class AvansAdmin(admin.ModelAdmin):
    list_display = ('id', 'zakaz', 'amount', 'time_create')
    list_editable = ('zakaz', 'amount')
    list_per_page = 12


@admin.register(Raskhod)
class AvansAdmin(admin.ModelAdmin):
    list_display = ('id', 'zakaz', 'amount', 'time_create')
    list_editable = ('zakaz', 'amount')
    list_per_page = 12
from django.contrib.auth import get_user_model
from django.db import models

class Auto(models.Model):
    marka = models.CharField(max_length=20)
    gos_num = models.CharField(max_length=10)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.marka + ' ' + self.gos_num


class ZakazNaryad(models.Model):
    auto = models.ForeignKey('Auto', on_delete=models.PROTECT, blank=True, default='Без номера')
    master = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='naryads', null=True, default=None)
    client = models.ForeignKey('Client', on_delete=models.PROTECT, blank=True, null=True)
    remont = models.CharField(max_length=250, blank=True)
    price = models.IntegerField(default=0)
    avans = models.IntegerField(default=0)
    raskhod = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True, null=True)
    time_update = models.DateTimeField(auto_now=True, null=True)


class Oplata(models.Model):
    zakaz = models.ForeignKey('ZakazNaryad', on_delete=models.PROTECT, related_name='oplata')
    amount = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True, null=True)


class Client(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(blank=True)
        
    def __str__(self):
        return self.name + ' ' + self.phone

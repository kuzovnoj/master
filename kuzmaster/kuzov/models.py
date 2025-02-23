from django.db import models

class Auto(models.Model):
    marka = models.CharField(max_length=20)
    gos_num = models.CharField(max_length=10)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)


class ZakazNaryad(models.Model):
    auto = models.ForeignKey('Auto', on_delete=models.PROTECT, blank=True, default='Без номера')
    master = models.ForeignKey('Kmaster', on_delete=models.PROTECT, blank=True, null=True)
    client = models.ForeignKey('Client', on_delete=models.PROTECT, blank=True, null=True)
    remont = models.TextField(max_length=250, blank=True)
    price = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True, null=True)
    time_update = models.DateTimeField(auto_now=True, null=True)

class Kmaster(models.Model):
    name = models.CharField(max_length=20)

class Client(models.Model):
    name = models.CharField(max_length=30)
    phone = models.IntegerField(blank=True)

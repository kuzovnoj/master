from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import RegexValidator


class Auto(models.Model):
    marka = models.CharField(max_length=20)
    gos_num = models.CharField(max_length=10)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.marka + ' ' + self.gos_num


class ZakazNaryad(models.Model):
    class Status(models.IntegerChoices):
        DONE = 0, 'Закрыт'
        OPEN = 1, 'Открыт'

    auto = models.ForeignKey('Auto', on_delete=models.PROTECT, blank=True, default='Без номера')
    master = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='naryads', null=True, default=None)
    client = models.ForeignKey('Client', on_delete=models.PROTECT, blank=True, null=True)
    remont = models.CharField(max_length=250, blank=True)
    price = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True, null=True)
    time_update = models.DateTimeField(auto_now=True, null=True)
    in_work = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.OPEN, verbose_name="Статус")

    def __str__(self):
        return 'Заказ-наряд' + str(self.id) + ' ' + self.auto.marka + ' ' + self.auto.gos_num


class Oplata(models.Model):
    zakaz = models.ForeignKey('ZakazNaryad', on_delete=models.PROTECT, related_name='oplata')
    amount = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True, null=True)


class Avans(models.Model):
    zakaz = models.ForeignKey('ZakazNaryad', on_delete=models.PROTECT, related_name='avans')
    amount = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)


class Raskhod(models.Model):
    zakaz = models.ForeignKey('ZakazNaryad', on_delete=models.PROTECT, related_name='raskhod')
    amount = models.IntegerField(default=0)
    time_create = models.DateTimeField(auto_now_add=True)


class Client(models.Model):
    name = models.CharField(max_length=30)
    phone_regex = RegexValidator(regex=r'^\+?[78]\d{10}$', message="Номер в формате: '+79999999999'")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list        
    def __str__(self):
        return self.name + ' ' + self.phone

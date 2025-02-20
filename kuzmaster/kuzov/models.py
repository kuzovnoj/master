from django.db import models

class auto(models.Model):
    marka = models.CharField(max_length=20)
    gos_num = models.CharField(max_length=10)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

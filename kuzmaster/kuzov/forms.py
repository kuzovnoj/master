from django import forms
from .models import Client, Auto, Kmaster, ZakazNaryad


class FormAuto(forms.ModelForm):

    class Meta:
        model = Auto
        fields = ['gos_num', 'marka']
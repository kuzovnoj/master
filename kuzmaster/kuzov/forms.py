from django import forms
from .models import Client, Auto, ZakazNaryad, Avans, Oplata, Raskhod


class FormAuto(forms.ModelForm):
    class Meta:
        model = Auto
        fields = ['gos_num', 'marka', 'photo']


class FormClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone']


class FormZakazNaryad(forms.ModelForm):
    class Meta:
        model = ZakazNaryad
        fields = ['auto', 'master', 'client', 'remont', 'price']
        

class FormAvans(forms.ModelForm):
    class Meta:
        model = Avans
        fields = ['zakaz', 'amount']


class FormOplata(forms.ModelForm):
    class Meta:
        model = Oplata
        fields = ['zakaz', 'amount']


class FormRaskhod(forms.ModelForm):
    class Meta:
        model = Raskhod
        fields = ['zakaz', 'amount', 'name', 'date', 'cheque']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}

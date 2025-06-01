from django import forms
from .models import Client, Auto, ZakazNaryad, Avans, Oplata, Raskhod


class FormAuto(forms.ModelForm):
    class Meta:
        model = Auto
        fields = ['gos_num', 'marka']


class FormClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone']


class FormZakazNaryad(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        self.pk_slug = kwargs.pop('pk_slug')
#    client = forms.ModelChoiceField(queryset=Client.objects.all(), initial=Client.objects.get(pk=int(pk_slug)))
    
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
        fields = ['zakaz', 'amount']

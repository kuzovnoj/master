from django import forms
from .models import Client, Auto, ZakazNaryad, Avans, Oplata, Raskhod
from .utils import send_telegram_message


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
    zakaz = forms.ModelChoiceField(queryset=ZakazNaryad.opened.all())
    class Meta:
        model = Avans
        fields = ['zakaz', 'amount', 'date', 'comment', 'cashier']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}
    
    def save(self, commit=True):
        instance = super().save(commit)
        
        master_id = ZakazNaryad.objects.get(pk=instance.zakaz.id).master.id
        # Отправка в Telegram после сохранения
        message = f"Аванс {instance.zakaz} Сумма: {instance.amount} {instance.comment}"
        send_telegram_message(message, master_id)
        return instance


class FormOplata(forms.ModelForm):
    zakaz = forms.ModelChoiceField(queryset=ZakazNaryad.opened.all())    
    class Meta:
        model = Oplata
        fields = ['zakaz', 'amount', 'date', 'cashier']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}
    
    def save(self, commit=True):
        instance = super().save(commit)
        
        master_id = ZakazNaryad.objects.get(pk=instance.zakaz.id).master.id
        # Отправка в Telegram после сохранения
        message = f"Оплата {instance.zakaz} Сумма: {instance.amount}"
        send_telegram_message(message, master_id)
        return instance


class FormRaskhod(forms.ModelForm):
    zakaz = forms.ModelChoiceField(queryset=ZakazNaryad.opened.all())
    class Meta:
        model = Raskhod
        fields = ['zakaz', 'amount', 'name', 'spare_part', 'date', 'cheque', 'cashier']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), 'spare_part': forms.CheckboxInput()}

    def save(self, commit=True):
        instance = super().save(commit)
        
        master_id = ZakazNaryad.objects.get(pk=instance.zakaz.id).master.id
        # Отправка в Telegram после сохранения
        if instance.spare_part:
            message = f"Запчасть оплачивает клиент {instance.zakaz} Сумма: {instance.amount} {instance.name}"
        else:
            message = f"{instance.zakaz} Сумма: {instance.amount} {instance.name}"
        send_telegram_message(message, master_id)
        return instance
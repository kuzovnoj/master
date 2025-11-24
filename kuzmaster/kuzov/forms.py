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
        
        # Отправка в Telegram после сохранения
        message = f"""
📨 <b>Новое сообщение с сайта</b>

👤 <b>Имя:</b> {instance.name}
📧 <b>Email:</b> {instance.email}
💬 <b>Сообщение:</b>
{instance.message}

🆔 <b>ID заявки:</b> #{instance.id}
        """
        
        send_telegram_message(message)
        return instance


class FormOplata(forms.ModelForm):
    zakaz = forms.ModelChoiceField(queryset=ZakazNaryad.opened.all())    
    class Meta:
        model = Oplata
        fields = ['zakaz', 'amount', 'date', 'cashier']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class FormRaskhod(forms.ModelForm):
    zakaz = forms.ModelChoiceField(queryset=ZakazNaryad.opened.all())
    class Meta:
        model = Raskhod
        fields = ['zakaz', 'amount', 'name', 'spare_part', 'date', 'cheque', 'cashier']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'}), 'spare_part': forms.CheckboxInput()}

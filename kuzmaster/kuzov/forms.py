from django import forms
from .models import Client, Auto, ZakazNaryad


class FormAuto(forms.ModelForm):

    class Meta:
        model = Auto
        fields = ['gos_num', 'marka']


#class FormZakazNaryad(forms.ModelForm):
#    
#    def form_valid(self, form):
#        w = form.save(commit=False)
#        w.master = self.request.user
#        return super().form_valid(form)    
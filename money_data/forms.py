from django import forms

from .models import MoneyLog

class MoneyForm(forms.ModelForm):
    class Meta:
        model=MoneyLog
        fields=['money_made', 'money_info', ]
        labels={'money_made': 'money made:', 'money_info': ''}
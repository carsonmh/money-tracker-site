from django import forms
from datetime import date

from .models import MoneyLog

class MoneyForm(forms.ModelForm):
    class Meta:
        model=MoneyLog
        fields=['money_made', 'money_info', 'date_added']
        labels={'money_made': 'Money Made', 'money_info': 'Extra Info', 'date_added': 'Date'}
        widgets = {
            'money_made': forms.NumberInput(attrs={
                'placeholder': 'Amount', 
                'class': 'form-input',
                'id': 'money_made-input',
            }),
            'money_info': forms.Textarea(attrs={
                'class': 'form-input',
                'id': 'money_info-input'
                }),
            'date_added': forms.DateInput(attrs={
                'class': 'form-input', 
                'type':'date',
                'id': 'date_added-input',
                'value': date.today()
                })
        }
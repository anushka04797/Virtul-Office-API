from django import forms
from .models import Slc


class CustomAddSLCForm(forms.ModelForm):
    class Meta:
        model = Slc
        fields = [
            'employee',
            'slc',
            'monthly_rate',
            'hourly_rate',
            'hourly_rate'
        ]

class CustomEditSLCForm(forms.ModelForm):
    class Meta:
        model = Slc
        fields = [
            'slc',
            'monthly_rate',
            'hourly_rate',
            'hourly_rate'
        ]
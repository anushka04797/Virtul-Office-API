from django import forms
from .models import HolidayCalender

class DropdownModelForm(forms.ModelForm):

    class Meta:
        model = DropdownModel
        fields = ('date_range',)
        widgets = {
            'date_range': forms.Select(choices=DropdownModel.CHOICES)
        }
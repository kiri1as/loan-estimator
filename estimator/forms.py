# forms.py
from django import forms
from .models import LoanApplication

class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = '__all__'

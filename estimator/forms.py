# forms.py
from django import forms
from .models import LoanApplication


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ["gender", "married", "dependents", "education", "self_employed", "applicant_income",
                  "coapplicant_income", "loan_amount", "loan_amount_term", "credit_history", "property_area"]

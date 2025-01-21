# models.py
from django.db import models

class LoanApplication(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARRIED_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    EDUCATION_CHOICES = [('Graduate', 'Graduate'), ('Not Graduate', 'Not Graduate')]
    SELF_EMPLOYED_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    PROPERTY_AREA_CHOICES = [('Urban', 'Urban'), ('Rural', 'Rural'), ('Semiurban', 'Semiurban')]

    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    Married = models.CharField(max_length=10, choices=MARRIED_CHOICES)
    Dependents = models.CharField(max_length=10)
    Education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    Self_Employed = models.CharField(max_length=10, choices=SELF_EMPLOYED_CHOICES)
    ApplicantIncome = models.FloatField()
    CoapplicantIncome = models.FloatField()
    LoanAmount = models.FloatField()
    Loan_Amount_Term = models.FloatField()
    Credit_History = models.FloatField()
    Property_Area = models.CharField(max_length=20, choices=PROPERTY_AREA_CHOICES)
    Loan_Status = models.CharField(max_length=10, null=True, blank=True)


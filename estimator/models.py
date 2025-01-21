# models.py
from django.db import models


class LoanApplication(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARRIED_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    CREDIT_HISTORY_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    EDUCATION_CHOICES = [('Graduate', 'Graduate'), ('Not Graduate', 'Not Graduate')]
    SELF_EMPLOYED_CHOICES = [('Yes', 'Yes'), ('No', 'No')]
    PROPERTY_AREA_CHOICES = [('Urban', 'Urban'), ('Rural', 'Rural'), ('Semiurban', 'Semiurban')]
    DEPENDENT_CHOICES = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]
    LOAN_TERM_CHOICES = [(12, 12), (24, 24), (36, 36), (48, 48), (60, 60), (84, 84), (120, 120), (160, 160), (180, 180),
                         (240, 240), (360, 360)]
    LOAN_AMOUNT_CHOICES = [(10, 10), (20, 20), (30, 30), (40, 40), (50, 50), (60, 60), (70, 70), (80, 80), (90, 90),
                           (100, 100), (120, 120), (150, 150), (180, 180), (200, 200), (250, 250), (300, 300),
                           (350, 350), (400, 400), (450, 450), (500, 500)]

    loan_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    married = models.CharField(max_length=3, choices=MARRIED_CHOICES)
    dependents = models.IntegerField(choices=DEPENDENT_CHOICES)
    education = models.CharField(max_length=20, choices=EDUCATION_CHOICES)
    self_employed = models.CharField(max_length=10, choices=SELF_EMPLOYED_CHOICES)
    applicant_income = models.FloatField()
    coapplicant_income = models.FloatField()
    loan_amount = models.IntegerField(choices=LOAN_AMOUNT_CHOICES)
    loan_amount_term = models.IntegerField(choices=LOAN_TERM_CHOICES)
    credit_history = models.CharField(max_length=3, choices=CREDIT_HISTORY_CHOICES)
    property_area = models.CharField(max_length=20, choices=PROPERTY_AREA_CHOICES)
    loan_status = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'estimator_loan_application'

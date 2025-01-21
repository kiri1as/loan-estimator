import joblib
import pandas as pd
from django.shortcuts import render

from .forms import LoanApplicationForm
from .models import LoanApplication


def predict(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)

        if form.is_valid():

            form_data = form.cleaned_data
            input_values = [
                form_data['gender'], form_data['married'], form_data['education'], form_data['self_employed'],
                form_data['dependents'], form_data['applicant_income'], form_data['coapplicant_income'],
                form_data['loan_amount'], form_data['loan_amount_term'],
                1 if form_data['credit_history'] == 'Yes' else 0, form_data['property_area']
            ]
            input_columns = [
                'Gender', 'Married', 'Education', 'Self_Employed',
                'Dependents', 'ApplicantIncome', 'CoapplicantIncome',
                'LoanAmount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area'
            ]
            model = joblib.load('data_model/loan_approval_model.pkl')
            model_in = pd.DataFrame(data=[input_values], columns=input_columns)
            model_out = model.predict(model_in)
            loan_accepted = 'Yes' if model_out == 1 else 'No'

            loan_application = LoanApplication(
                gender=form_data['gender'],
                married=form_data['married'],
                dependents=form_data['dependents'],
                education=form_data['education'],
                self_employed=form_data['self_employed'],
                applicant_income=form_data['applicant_income'],
                coapplicant_income=form_data['coapplicant_income'],
                loan_amount=form_data['loan_amount'],
                loan_amount_term=form_data['loan_amount_term'],
                credit_history=form_data['credit_history'],
                property_area=form_data['property_area'],
                loan_status= loan_accepted,
            )
            loan_application.save()
            print(loan_application.loan_id)

            return render(request, 'estimation.html', {'result': loan_accepted, 'id': loan_application.loan_id})
    else:
        form = LoanApplicationForm()
    return render(request, 'application_form.html', {'form': form})

def application_list(request):
    applications = LoanApplication.objects.all()
    return render(request, 'application_list.html', {'applications': applications})

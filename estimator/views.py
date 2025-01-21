import base64
from io import BytesIO

import joblib
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import pandas as pd
import seaborn as sns
from django.shortcuts import render

from data_model.creation_script import prepared_data
from .forms import LoanApplicationForm
from .models import LoanApplication


def loan_estimation(request):
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

            return render(request, 'result.html', {'result': loan_accepted, 'id': loan_application.loan_id})
    else:
        form = LoanApplicationForm()
    return render(request, 'application.html', {'form': form})


def loan_data_plots(request):
    df = pd.read_csv('data_model/loan_data.csv')
    dataframe, categorical_features, numerical_features = prepared_data(df)

    plt.figure(figsize=(8, 6))
    sns.countplot(x='Loan_Status', hue='Loan_Status', data=df, palette='viridis')
    plt.title('Distribution of Loan_Status')
    buffer_loan_status = BytesIO()
    plt.savefig(buffer_loan_status, format='png')
    buffer_loan_status.seek(0)
    loan_status_plot = base64.b64encode(buffer_loan_status.getvalue()).decode('utf-8')
    plt.close()

    plt.figure(figsize=(12, 8))
    sns.histplot(df['LoanAmount'], kde=True)
    plt.title('Loan Amount Distribution')
    buffer_loan_amount = BytesIO()
    plt.savefig(buffer_loan_amount, format='png')
    buffer_loan_amount.seek(0)
    loan_amount_plot = base64.b64encode(buffer_loan_amount.getvalue()).decode('utf-8')
    plt.close()

    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Loan_Status', y='ApplicantIncome', data=df)
    plt.title('Applicant Income vs Loan Status')
    buffer_income_vs_loan = BytesIO()
    plt.savefig(buffer_income_vs_loan, format='png')
    buffer_income_vs_loan.seek(0)
    income_vs_loan_plot = base64.b64encode(buffer_income_vs_loan.getvalue()).decode('utf-8')
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.countplot(x='Credit_History', hue='Loan_Status', data=df, palette='Set2')
    plt.title('Loan Status by Credit History')
    buffer_credit_history = BytesIO()
    plt.savefig(buffer_credit_history, format='png')
    buffer_credit_history.seek(0)
    credit_history_plot = base64.b64encode(buffer_credit_history.getvalue()).decode('utf-8')
    plt.close()

    correlation_matrix = df[numerical_features].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    buffer_correlation_matrix = BytesIO()
    plt.savefig(buffer_correlation_matrix, format='png')
    buffer_correlation_matrix.seek(0)
    correlation_matrix_plot = base64.b64encode(buffer_correlation_matrix.getvalue()).decode('utf-8')
    plt.close()

    return render(request, 'charts.html', {
        'loan_status_plot': loan_status_plot,
        'loan_amount_plot': loan_amount_plot,
        'income_vs_loan_plot': income_vs_loan_plot,
        'credit_history_plot': credit_history_plot,
        'correlation_matrix_plot': correlation_matrix_plot,
    })

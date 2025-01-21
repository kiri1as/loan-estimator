from django.shortcuts import render
from .models import LoanApplication
from .forms import LoanApplicationForm
import joblib


def predict(request):
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST)

        if form.is_valid():
            model = joblib.load('loan_approval_model.pkl')
            data = form.cleaned_data

            loan_application = LoanApplication(
                Gender=data['Gender'],
                Married=data['Married'],
                Dependents=data['Dependents'],
                Education=data['Education'],
                Self_Employed=data['Self_Employed'],
                ApplicantIncome=data['ApplicantIncome'],
                CoapplicantIncome=data['CoapplicantIncome'],
                LoanAmount=data['LoanAmount'],
                Loan_Amount_Term=data['Loan_Amount_Term'],
                Credit_History=data['Credit_History'],
                Property_Area=data['Property_Area']
            )

            input_data = [data['Gender'], data['Married'], data['Dependents'], data['Education'], data['Self_Employed'],
                          data['ApplicantIncome'], data['CoapplicantIncome'], data['LoanAmount'],
                          data['Loan_Amount_Term'], data['Credit_History'], data['Property_Area']]

            prediction = model.predict([input_data])
            result = 'Approved' if prediction[0] == 1 else 'Rejected'
            loan_application.Loan_Status = result
            loan_application.save()

            return render(request, 'estimation.html', {'result': result, 'application': loan_application})
    else:
        form = LoanApplicationForm()
    return render(request, 'application_form.html', {'form': form})

def application_list(request):
    applications = LoanApplication.objects.all()
    return render(request, 'application_list.html', {'applications': applications})


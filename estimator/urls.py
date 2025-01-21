from django.urls import path
from . import views

urlpatterns = [
    path('', views.loan_estimation, name='predict'),
    path('predict/', views.loan_estimation, name='predict'),
    path('predict/charts', views.loan_data_plots, name='charts'),
]
# coding: utf-8
from django.urls import path
from .signup_views import WorkerCreateView, SuccessView, FailureView, CompanyCreateView

urlpatterns = [
    path('worker/', WorkerCreateView.as_view()),
    path("company/", CompanyCreateView.as_view()),
    path('success/', SuccessView.as_view()),
    path('failure/', FailureView.as_view()),
]

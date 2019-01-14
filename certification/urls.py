# coding: utf-8
from django.urls import path
from rest_framework import routers
from .viewset import UserViewSet
from .views import UserCreateView, SuccessView, FailureView, CompanyCreateView

router = routers.DefaultRouter()
router.register(r'login', UserViewSet)


urlpatterns = [
    path('worker', UserCreateView.as_view()),
    path("company", CompanyCreateView.as_view()),
    path('success', SuccessView.as_view()),
    path('failure', FailureView.as_view()),
]

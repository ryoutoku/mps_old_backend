# coding: utf-8
from django.urls import path
from rest_framework import routers
from .viewset import UserViewSet
from .views import UserCreateView, SuccessView, FailureView

router = routers.DefaultRouter()
router.register(r'login', UserViewSet)


urlpatterns = [
    path('', UserCreateView.as_view()),
    path('success', SuccessView.as_view()),
    path('failure', FailureView.as_view()),
]

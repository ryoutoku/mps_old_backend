# coding: utf-8

from rest_framework import routers
from .viewset import WorkerViewSet, CareerViewSet, BankViewSet

router = routers.DefaultRouter()
router.register(r'profile', WorkerViewSet)
router.register(r"bank", BankViewSet)
router.register(r'careers', CareerViewSet)

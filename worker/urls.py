# coding: utf-8

from rest_framework import routers
from .viewset import WorkerViewSet, CareerViewSet

router = routers.DefaultRouter()
router.register(r'workers', WorkerViewSet)
router.register(r'careers', CareerViewSet)

# coding: utf-8

from rest_framework import routers
from .viewset import UserViewSet, CareerViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'careers', CareerViewSet)

# coding: utf-8

from rest_framework import routers
from .viewset import CompanyViewSet, ProjectViewSet


router = routers.DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'projects', ProjectViewSet)

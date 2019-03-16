# coding: utf-8

from rest_framework.routers import DefaultRouter
from .viewset import CompanyBasicInfoViewSet, CompanyStaffViewSet, ProjectViewSet

from utility.router import SameURLRouter

router = SameURLRouter()
router.register('info', CompanyBasicInfoViewSet)
router.register('staff', CompanyStaffViewSet)

default_router = DefaultRouter()
default_router.register('projects', ProjectViewSet)

urlpatterns = router.urls + default_router.urls

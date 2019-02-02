# coding: utf-8

from rest_framework.routers import DefaultRouter
from .viewset import CompanyViewSet, ProjectViewSet

from utility.router import SameURLRouter

router = SameURLRouter()
router.register('info', CompanyViewSet)

default_router = DefaultRouter()
default_router.register('projects', ProjectViewSet)


urlpatterns = router.urls + default_router.urls

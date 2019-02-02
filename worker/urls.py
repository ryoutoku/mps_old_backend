# coding: utf-8
from rest_framework.routers import DefaultRouter
from .viewset import WorkerViewSet, ResumeViewSet, BankViewSet

from utility.router import SameURLRouter

router = SameURLRouter()
router.register("info", WorkerViewSet)
router.register("bank", BankViewSet)

default_router = DefaultRouter()
default_router.register("resumes", ResumeViewSet)

urlpatterns = router.urls + default_router.urls

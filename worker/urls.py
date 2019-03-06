# coding: utf-8
from rest_framework.routers import DefaultRouter
from .viewset import WorkerBasicInfoViewSet, WorkerConditionViewSet, ResumeViewSet, TechnologyViewSet

from utility.router import SameURLRouter

router = SameURLRouter()
router.register("info", WorkerBasicInfoViewSet)
router.register("condition", WorkerConditionViewSet)

default_router = DefaultRouter()
default_router.register("resumes", ResumeViewSet)
default_router.register("technologies", TechnologyViewSet)

urlpatterns = router.urls + default_router.urls

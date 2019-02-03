# coding: utf-8
from rest_framework import routers
from .viewset import QuestionViewSet, AnswerViewSet

router = routers.DefaultRouter()
router.register(r'question', QuestionViewSet)
router.register(r"answer", AnswerViewSet)


urlpatterns = router.urls

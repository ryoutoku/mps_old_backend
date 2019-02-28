# coding: utf-8

from rest_framework import routers
from .viewset import LoginViewSet, LogoutViewSet, SingUpViewSet

router = routers.DefaultRouter()
router.register(r"login", LoginViewSet)
router.register(r"logout", LogoutViewSet)
router.register(r"signup", SingUpViewSet)


urlpatterns = router.urls

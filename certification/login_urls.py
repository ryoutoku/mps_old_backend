# coding: utf-8

from rest_framework import routers
from .login_viewset import LoginViewSet, LogoutViewSet

router = routers.DefaultRouter()
router.register(r"login", LoginViewSet)
router.register(r"logout", LogoutViewSet)

# coding: utf-8
from django.contrib.auth import login, logout
from rest_framework import viewsets, mixins, permissions, authentication
from rest_framework.response import Response

from .models import User
from .selializer import LoginSerializer, LogoutSerializer


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):
    """ログインを提供するAPIのクラス
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        account = "worker"
        if hasattr(request.user, "company"):
            account = "company"

        return Response({"account": account})


class LogoutViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    """ログアウトを提供するAPIのクラス
    """
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = LogoutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        logout(request)
        return Response()

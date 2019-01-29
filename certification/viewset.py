from rest_framework import viewsets, filters
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response

from .models import User
from .selializer import LoginSerializer, LogoutSerializer

from django.contrib.auth import login, logout

from rest_framework import views, permissions, authentication


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class LoginViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ログインを提供するAPIのクラス
    """
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication,)

    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response()


class LogoutViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """ログアウトを提供するAPIのクラス
    """
    queryset = User.objects.all()
    serializer_class = LogoutSerializer

    def create(self, request):
        logout(request)
        return Response()

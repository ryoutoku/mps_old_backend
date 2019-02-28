# coding: utf-8
from django.contrib.auth import login, logout
from rest_framework import viewsets, mixins, permissions, authentication
from rest_framework.response import Response
from rest_framework import status

from .models import User, SignUpToken, TOKEN_ATTRIBUTE
from worker.models import Worker, WorkerBank
from company.models import Company
from .selializer import LoginSerializer, LogoutSerializer, SingUpSerializer


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

        return Response({"account": account}, status=status.HTTP_200_OK)


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
        return Response(status=status.HTTP_200_OK)


class SingUpViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = SingUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['token']

        user_token = SignUpToken.objects.filter(token=token).first()

        account = None
        for token_attr in TOKEN_ATTRIBUTE:
            if token_attr[0] == user_token.attribute:
                account = token_attr[1]
                break

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = User.objects.create(email=email, password=password)

        if account == "worker":
            self._create_worker(user)
        else:
            self._create_company(user)

        return Response({"account": account}, status=status.HTTP_201_CREATED)

    def _create_worker(self, user):
        worker = Worker.objects.create(account=user)
        worker.save()
        worker_bank = WorkerBank.objects.create(worker=worker)
        worker_bank.save()

    def _create_company(self, user):
        company = Company.objects.create(account=user)
        company.save()

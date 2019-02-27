# coding: utf-8
from django.contrib.auth import login, logout
from rest_framework import viewsets, mixins, permissions, authentication
from rest_framework.response import Response

from .models import User
from .selializer import LoginSerializer, LogoutSerializer


from django.views.generic import TemplateView, CreateView
from django.utils.timezone import utc
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from rest_framework import views, permissions, authentication

from rest_framework import generics

from datetime import datetime
from .models import User, SignUpToken
from .forms import WorkerModelForm, CompanyModelForm


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


class SignUpBaseCreateView(CreateView):

    model = User
    form_class = None
    template_name = "./signup/index.html"
    success_url = "./success"
    failure_url = "./failure"

    def get(self, request, attribute, **kwargs):
        token = request.GET.get("token", default=None)

        if token is None:
            return HttpResponseRedirect(self.failure_url)

        signup_token = SignUpToken.objects.filter(
            token=token, attribute=attribute).first()

        tmp = SignUpToken.objects.filter(token=token).first()
        if signup_token is None:
            return HttpResponseRedirect(self.failure_url)

        now = datetime.utcnow().replace(tzinfo=utc)
        if signup_token.expiration_date <= now:
            HttpResponseRedirect(self.failure_url)

        return super().get(request, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.password = make_password(user.password)
        user.save()
        return HttpResponseRedirect(self.success_url)


class WorkerCreateView(SignUpBaseCreateView):
    worker = 1
    form_class = WorkerModelForm

    def get(self, request, **kwargs):
        return super().get(request, self.worker, **kwargs)


class CompanyCreateView(SignUpBaseCreateView):
    company = 0
    form_class = CompanyModelForm

    def get(self, request, **kwargs):
        return super().get(request, self.company, **kwargs)

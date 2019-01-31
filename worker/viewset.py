import django_filters
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import generics

from .models import Worker, Resume, WorkerBank
from .selializer import WorkerSerializer, ResumeSerializer, BankSerializer

from django.conf import settings


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return (request.user is not None) & hasattr(request.user, "worker")


class WorkerViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin,):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsWorker)

    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset.filter(pk=request.user.worker.id).update(
            **serializer.data)
        return Response(serializer.data)

    def list(self, request):
        serializer = self.get_serializer_class()(
            self.queryset.filter(pk=request.user.worker.id).first())
        return Response(serializer.data)


class BankViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin, mixins.ListModelMixin,):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    queryset = WorkerBank.objects.all()
    serializer_class = BankSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset.filter(pk=request.user.worker.bank.id).update(
            **serializer.data)
        return Response(serializer.data)

    def list(self, request):
        serializer = self.get_serializer_class()(
            self.queryset.filter(pk=request.user.worker.bank.id).first())
        return Response(serializer.data)


class ResumeViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin,):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset.filter(pk=request.user.worker.bank.id).update(
            **serializer.data)
        return Response(serializer.data)

    def list(self, request):
        serializer = self.get_serializer_class()(
            self.queryset.filter(pk=request.user.worker.bank.id).first())
        return Response(serializer.data)

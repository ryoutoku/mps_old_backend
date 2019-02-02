# coding: utf-8
from rest_framework.views import APIView
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
                    mixins.ListModelMixin, mixins.UpdateModelMixin):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsWorker,)

    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.request.user.worker.id).first()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset()
        queryset.update(**serializer.data)
        return Response(serializer.data)


class BankViewSet(viewsets.GenericViewSet,
                  mixins.UpdateModelMixin, mixins.ListModelMixin,):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated and IsWorker,)

    queryset = WorkerBank.objects.all()
    serializer_class = BankSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(worker=self.request.user.worker).first()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset()
        queryset.update(**serializer.data)
        return Response(serializer.data)


class ResumeViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated and IsWorker,)

    queryset = Resume.objects.order_by('started_at')
    serializer_class = ResumeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(worker=self.request.user.worker).all()
        return queryset

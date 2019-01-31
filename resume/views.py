# coding: utf-8
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import generics

from .models import Worker, Resume, WorkerBank
from .selializer import WorkerSerializer, ResumeSerializer, BankSerializer

from django.conf import settings


class WorkerViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin,):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated, IsWorker)

    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.request.user.worker.id)
        self.kwargs["pk"] = self.request.user.worker.id
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset.filter(pk=request.user.worker.id).update(
            **serializer.data)
        return Response(serializer.data)

    def list(self, request):
        data = self.get_object()
        serializer = self.get_serializer_class()(data)
        return Response(serializer.data)


class BankViewSet(viewsets.GenericViewSet,
                  mixins.CreateModelMixin, mixins.ListModelMixin,):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, IsWorker)

    queryset = WorkerBank.objects.all()
    serializer_class = BankSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(worker=self.request.user.worker)
        self.kwargs["pk"] = self.request.user.worker.bank.id
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset.filter(pk=request.user.worker.bank.id).update(
            **serializer.data)
        return Response(serializer.data)

    def list(self, request):
        data = self.get_object()
        serializer = self.get_serializer_class()(data)
        return Response(serializer.data)


class ResumeViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, IsWorker)

    queryset = Resume.objects.order_by('started_at')
    serializer_class = ResumeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(worker=self.request.user.worker)
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.data)
        data["worker"] = request.user.worker
        Resume.objects.create(**data).save()

        return Response(serializer.data)

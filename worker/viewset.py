# coding: utf-8
from rest_framework.views import APIView
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from .models import WorkerBasicInfo, WorkerCondition, Resume
from .selializer import WorkerBasicInfoSerializer, WorkerConditionSerializer, ResumeSerializer

from utility.permission import IsWorker


class WorkerBasicInfoViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin, mixins.UpdateModelMixin):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsWorker,)

    queryset = WorkerBasicInfo.objects.all()
    serializer_class = WorkerBasicInfoSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.first()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(account=self.request.user).all()
        return queryset

    def list(self, request, *args, **kwargs):
        data = self.get_queryset().first()
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.data["is_activated"] = True
        queryset = self.get_queryset()
        queryset.update(**serializer.data)
        return Response(serializer.data)


class WorkerConditionViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin, mixins.UpdateModelMixin):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsWorker,)

    queryset = WorkerCondition.objects.all()
    serializer_class = WorkerConditionSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.first()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(worker=self.request.user.worker).all()
        return queryset

    def list(self, request, *args, **kwargs):
        data = self.get_queryset().first()
        serializer = self.get_serializer(data)
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

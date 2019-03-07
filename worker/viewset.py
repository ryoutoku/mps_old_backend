# coding: utf-8
from rest_framework.views import APIView
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from .models import WorkerBasicInfo, WorkerCondition, Resume, Technology
from .selializer import WorkerBasicInfoSerializer, WorkerConditionSerializer, ResumeSerializer, TechnologySerializer

from utility.permission import IsWorker


class WorkerBasicInfoViewSet(viewsets.GenericViewSet,
                             mixins.ListModelMixin, mixins.UpdateModelMixin):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsWorker,)

    queryset = WorkerBasicInfo.objects.all()
    serializer_class = WorkerBasicInfoSerializer

    def get_object(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(account=self.request.user)
        return queryset.first()

    def list(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
        queryset = super().get_queryset()
        queryset = queryset.filter(worker=self.request.user.worker)
        return queryset.first()

    def list(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.get_object()
        serializer.update(instance, serializer.data)
        instance.save()
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


class TechnologyViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    queryset = Technology.objects.order_by('name')
    serializer_class = TechnologySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.all()
        return queryset

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
        queryset = self.get_queryset()
        return queryset.first()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(account=self.request.user).all()

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
        queryset = self.get_queryset()
        return queryset.first()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(worker=self.request.user.worker).all()

    def list(self, request, *args, **kwargs):
        data = self.get_object()
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        serializer.update(instance, serializer.data)

        responseSerializer = WorkerConditionSerializer(instance)
        return Response(responseSerializer.data)


class ResumeViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated and IsWorker,)

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(worker=self.request.user.worker).all()

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_object()
        serializer.update(instance, serializer.data)

        data = self.get_queryset()
        response_serializer = self.serializer_class(data, many=True)
        return Response(response_serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        worker = request.user.worker
        resume = Resume(worker=worker)
        serializer.update(resume, serializer.data)

        data = self.get_queryset()
        response_serializer = self.serializer_class(data, many=True)
        return Response(response_serializer.data)


class TechnologyViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer

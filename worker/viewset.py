# coding: utf-8
from rest_framework.views import APIView
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django_filters.rest_framework import FilterSet, ChoiceFilter

from .models import WorkerBasicInfo, WorkerCondition, Resume, Technology
from .models import PROJECT_SCALE_CHOICES
from .selializer import WorkerBasicInfoSerializer, WorkerConditionSerializer, ResumeSerializer, TechnologySerializer

from utility.permission import IsWorker, IsCompany

import time


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
    permission_classes = (IsAuthenticated and IsWorker, )

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        data = self.get_queryset()
        response_serializer = self.serializer_class(data, many=True)
        return Response(status=status.HTTP_202_ACCEPTED, data=response_serializer.data)


class TechnologyViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer


class SearchResumesFilter(FilterSet):
    project_scale = ChoiceFilter(choices=PROJECT_SCALE_CHOICES)

    class Meta:
        model = Resume
        fields = ("project_scale", )


class SearchResumesViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated and IsCompany, )

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    filter_class = SearchResumesFilter

    def list(self, request, *args, **kwargs):
        print(request)
        print(args)
        print(kwargs)
        return super().list(request, *args, **kwargs)

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
        queryset = queryset.filter(account=self.request.user).all()
        return queryset

    def list(self, request, *args, **kwargs):
        data = self.get_queryset().first()
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.data.is_activate = self._get_is_activate(serializer.data)
        queryset = self.get_queryset()
        queryset.update(**serializer.data)
        return Response(serializer.data)

    def _get_is_activate(self, data):
        """必須入力が入力されているか確認
        """
        last_name = data.last_name
        first_name = data.first_name
        last_name_kana = data.last_name_kana
        first_name_kana = data.first_name_kana
        address = data.address

        if last_name is None or \
                last_name_kana is None or \
                first_name is None or \
                first_name_kana is None or \
                address is None:
            return False
        return True


class ResumeViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated and IsWorker,)

    queryset = Resume.objects.order_by('started_at')
    serializer_class = ResumeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(account=self.request.user).all()
        return queryset

    def perform_create(self, serializer):
        data = serializer.data
        data["worker"] = self.request.user.worker
        obj = Resume.objects.create(**data)
        obj.clean()
        obj.save()

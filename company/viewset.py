# coding: utf-8
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from .models import CompanyBasicInfo, CompanyStaff, Project
from .selializer import CompanyBasicInfoSerializer, CompanyStaffSerializer, ProjectSerializer

from utility.permission import IsCompany
import time


class CompanyBasicInfoViewSet(viewsets.GenericViewSet,
                              mixins.ListModelMixin, mixins.UpdateModelMixin):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsCompany, )

    queryset = CompanyBasicInfo.objects.all()
    serializer_class = CompanyBasicInfoSerializer

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(account=self.request.user).all()
        return queryset

    def list(self, request, *args, **kwargs):
        time.sleep(2)
        data = self.get_object()
        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset()
        queryset.update(**serializer.data)
        return Response(serializer.data)


class CompanyStaffViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin, mixins.UpdateModelMixin):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsCompany, )

    queryset = CompanyStaff.objects.all()
    serializer_class = CompanyStaffSerializer

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(company=self.request.user.company).all()

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


class ProjectViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsCompany, )

    queryset = Project.objects.order_by("start_term")
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(company=self.request.user.company).all()
        return queryset

    def perform_create(self, serializer):
        data = serializer.data
        data["company"] = self.request.user.company
        obj = Project.objects.create(**data)
        obj.clean()
        obj.save()

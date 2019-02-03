# coding: utf-8
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics

from .models import Company, Project
from .selializer import CompanySerializer, ProjectSerializer

from utility.permission import IsCompany


class CompanyViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin, mixins.UpdateModelMixin):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsCompany, )

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.request.user.company.id).all()
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        serializer = self.get_serializer(queryset, many=False)
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

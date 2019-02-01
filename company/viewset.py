# coding: utf-8
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.response import Response
from rest_framework import generics

from .models import Company, Project
from .selializer import CompanySerializer, ProjectSerializer


class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return (request.user is not None) & hasattr(request.user, "company")


class CompanyViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin, mixins.ListModelMixin,):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (IsAuthenticated and IsCompany, )

    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(pk=self.request.user.company.id)
        self.kwargs["pk"] = self.request.user.company.id
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.queryset.filter(pk=request.user.company.id).update(
            **serializer.data)
        return Response(serializer.data)

    def list(self, request):
        data = self.get_object()
        serializer = self.get_serializer_class()(data)
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
        queryset = queryset.filter(company=self.request.user.company)
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = dict(serializer.data)
        data["company"] = request.user.company
        Project.objects.create(**data).save()

        return Response(serializer.data)

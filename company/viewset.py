import django_filters
from rest_framework import viewsets, filters

from .models import Company, Project
from .selializer import CompanySerializer, ProjectSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

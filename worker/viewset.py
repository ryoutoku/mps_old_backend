import django_filters
from rest_framework import viewsets, filters

from .models import Worker, Career
from .selializer import WorkerSerializer, CareerSerializer


class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

import django_filters
from rest_framework import viewsets, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Worker, Career, WorkerBank
from .selializer import WorkerSerializer, CareerSerializer, BankSerializer


class WorkerViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def list(self, request):
        model = request.user
        print(model.id)
        return super().list(request)


class BankViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    queryset = WorkerBank.objects.all()
    serializer_class = BankSerializer


class CareerViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    queryset = Career.objects.all()
    serializer_class = CareerSerializer

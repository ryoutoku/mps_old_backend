import django_filters
from rest_framework import viewsets, filters, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Worker, Resume, WorkerBank
from .selializer import WorkerSerializer, ResumeSerializer, BankSerializer


class WorkerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def list(self, request):
        model = request.user
        serializer = self.serializer_class(
            self.queryset.filter(pk=model.worker.id).first())
        return Response(serializer.data)


class BankViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    queryset = WorkerBank.objects.all()
    serializer_class = BankSerializer

    def list(self, request):
        model = request.user
        serializer = self.serializer_class(
            self.queryset.filter(pk=model.worker.bank.id).first())
        return Response(serializer.data)


class ResumeViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated,)

    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

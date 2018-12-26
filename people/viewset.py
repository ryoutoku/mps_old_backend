import django_filters
from rest_framework import viewsets, filters

from .models import User, Career
from .selializer import UserSerializer, CareerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

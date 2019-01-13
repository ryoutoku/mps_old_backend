import django_filters
from rest_framework import viewsets, filters
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response

from .models import User
from .selializer import UserSerializer


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

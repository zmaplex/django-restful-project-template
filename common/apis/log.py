from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from common.models.log import LoginLogModel
from common.serializers.log import LoginLogModelSerializer


class LoginLogView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = LoginLogModel.objects.all()
    serializer_class = LoginLogModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]



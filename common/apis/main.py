from django.conf import settings
from common.models.main import MainModel
from common.permission import HasAccessKeyVerifySignaturePermission
from common.serializers.main import MainSerializer
from django_filters import rest_framework
from rest_framework import filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet


class MainView(ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MainModel.objects.all()
    serializer_class = MainSerializer
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    lookup_field = "id"

    @action(methods=["get"], detail=True, permission_classes=[permissions.AllowAny])
    def ping(self, request, *args, **kwargs):
        if settings.DEBUG:
            return Response({"message": "pong"})
        else:
            return Response({"message": "Not allowed!"}, status=403)



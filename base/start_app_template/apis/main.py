from django.conf import settings
from django_filters import rest_framework
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from base.start_app_template.models.main import MainModel
from base.start_app_template.serializers.main import MainModelSerializer


class MainView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MainModel.objects.all()
    serializer_class = MainModelSerializer
    filter_backends = (
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    lookup_field = "id"

    @action(methods=["get"], detail=False, permission_classes=[permissions.AllowAny])
    def ping(self, request, *args, **kwargs):
        if settings.DEBUG:
            return Response({"message": "pong"})
        else:
            return Response({"message": "Not allowed!"}, status=403)

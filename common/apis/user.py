from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import viewsets
from rest_framework.response import Response
from common.models.log import LoginLogModel

from common.models.user import User
from common.permission import HasAccessKeyVerifySignaturePermission
from common.serializers.user import (
    CreateUserSerializer,
    AdminUserSerializer,
    UserLoginSerializer,
    UserSerializer,
    UpdatePasswordSerializer,
    UserLoginResSerializer,
)


class AdminUserView(viewsets.ModelViewSet):
    permission_classes = permissions.IsAdminUser
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username"]
    filterset_fields = ["username", "email"]

    def destroy(self, request, *args, **kwargs):
        user = self.get_object().user
        user.is_active = False
        user.save()
        return Response("成功限制用户登录")


class UserView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["username"]
    filterset_fields = ["username", "email"]

    def get_queryset(self):
        
        user = self.request.user
        if user.is_superuser:
            return self.queryset.order_by("-id")
        return self.queryset.filter(pk=self.request.user.id).order_by("-id")
    
    @action(
        methods=["get"],
        detail=False,
        permission_classes=[HasAccessKeyVerifySignaturePermission],
    )
    def ping_with_aceess_key(self, request, *args, **kwargs):
        """
        适用场景：提供给第三方 API 调用
        通过 AccessKey 和 SecretAccessKey 进行签名验证，如果验证通过后把请求的数据返回
        """
        response = {"data": None}
        if request.data:
            response["data"] = request.data.dict()
        if request.query_params:
            response["query_params"] = request.query_params.dict()
        return Response(response)

    @transaction.atomic
    @action(methods=["POST"], detail=False, permission_classes=[permissions.AllowAny])
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return self.base_response(data=serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(responses={"200": UserLoginResSerializer})
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        serializer_class=UserLoginSerializer,
    )
    def login(self, request, *args, **kwargs):
        """
        登录接口，email 与 username 至少传一项
        """
        serializer = UserLoginSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            user: User = None
            token, user = serializer.save()
            return Response(
                {"token": f"{token}", "username": user.username, "email": user.email},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(methods=["POST"], detail=False, permission_classes=[permissions.AllowAny])
    def forget_password(self, request, *args, **kwargs):
        return Response(
            {"msg": "该接口尚未实现"}, status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    # @vary_on_headers('anonymous', 'authorization')
    # @method_decorator(cache_page(30))
    @action(
        methods=["get"], detail=False, permission_classes=[permissions.IsAuthenticated]
    )
    def status(self, request: Request, *args, **kwargs):
        user: User = request.user
        serializer = UserSerializer(user)
        # return Respon (serializer.data)
        return Response(serializer.data)

    @extend_schema(responses=UserSerializer)
    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UpdatePasswordSerializer,
    )
    def update_password(self, request: Request, *args, **kwargs):
        serializer = UpdatePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            data = serializer.save()
            return Response(data)



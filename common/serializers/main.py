from common.models.main import MainModel
from rest_framework import serializers


class MainSerializer(serializers.Serializer):
    def get_user(self):
        """
        获取用户，初始化序列的时候，请添加 context={'request': request}，
        :return:
        """
        request = self.context.get("request", None)
        if request:
            return request.user

        raise RuntimeError(
            f"无法获取用户，请在初始化{self.__class__.__name__}的时候添加参数 context={'request': request}"
        )


class MainModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainModel
        fields = "__all__"

    def get_user(self):
        """
        获取用户，初始化序列的时候，请添加 context={'request': request}，
        :return:
        """
        request = self.context.get("request", None)
        if request:
            return request.user

        raise RuntimeError(
            f"无法获取用户，请在初始化{self.__class__.__name__}的时候添加参数 context={'request': request}"
        )

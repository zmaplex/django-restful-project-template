from common.models.log import LoginLogModel
from rest_framework import serializers



class LoginLogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginLogModel
        fields = "__all__"
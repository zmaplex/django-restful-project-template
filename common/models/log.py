from django.db import models

from base.basemodel import BaseModel


class LoginLogModel(BaseModel):
    user = models.ForeignKey(
        "User", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="用户"
    )
    user_email = models.CharField(null=True, verbose_name="用户邮箱", max_length=128)
    username = models.CharField(null=True, verbose_name="用户名", max_length=128)
    user_role = models.CharField(null=True, verbose_name="用户角色", max_length=128)
    logging_ip = models.CharField(verbose_name="登录IP", max_length=128)
    auth_result = models.BooleanField(default=False, verbose_name="认证结果")
    message = models.CharField(null=True, verbose_name="消息", max_length=128)



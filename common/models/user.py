from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    # 主要增加邮箱地址唯一约束
    email = models.EmailField("邮件地址", blank=True, unique=True)
    avatar = models.URLField(default=None, blank=True, null=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(User, self).save(*args, **kwargs)
        if is_new:
            token, _ = Token.objects.get_or_create(user=self)
            Token.objects.filter(pk=token.key).update(key=token.generate_key())


class UserRelationPermissionModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户")
    permissions_code = models.ManyToManyField(
        "UserPermissionCodeModel", blank=True, verbose_name="用户权限"
    )
    permissions_groups = models.ManyToManyField(
        "UserPermissionGroupModel", blank=True, verbose_name="用户组权限"
    )

    class Meta:
        verbose_name = "用户权限"
        verbose_name_plural = verbose_name
        unique_together = ("user",)

    def __str__(self):
        return self.user.username


# 增加用户权限与用户组
class UserPermissionCodeModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="权限名称")
    code = models.CharField(max_length=100, verbose_name="权限代码")
    desc = models.CharField(max_length=100, verbose_name="权限描述")

    class Meta:
        verbose_name = "权限代码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserPermissionGroupModel(models.Model):
    name = models.CharField(max_length=100, verbose_name="用户组名称")
    code = models.CharField(max_length=100, verbose_name="用户组代码")
    desc = models.CharField(max_length=100, verbose_name="用户组描述")
    permissions = models.ManyToManyField(UserPermissionCodeModel, verbose_name="用户组权限")

    class Meta:
        verbose_name = "用户组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

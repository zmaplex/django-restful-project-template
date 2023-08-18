from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="创建日期", verbose_name="创建日期"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="更新日期", verbose_name="最后修改"
    )

    class Meta:
        abstract = True

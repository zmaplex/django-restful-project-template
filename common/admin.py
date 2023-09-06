# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from common.models.akas import AccessKeyAndSecretModel


from common.models.user import  User , UserPermissionGroupModel, UserPermissionCodeModel, UserRelationPermissionModel

# Register your models here.
admin.site.register(User, UserAdmin)



@admin.register(UserPermissionGroupModel)
class UserPermissionGroupModelAdmin(admin.ModelAdmin):

    pass

@admin.register(UserRelationPermissionModel)
class UserRelationPermissionModelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserPermissionCodeModel)
class UserPermissionModelAdmin(admin.ModelAdmin):
    pass

@admin.register(AccessKeyAndSecretModel)
class AccessKeyAndSecretModelAdmin(admin.ModelAdmin):
    pass
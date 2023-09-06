from rest_framework.permissions import BasePermission
from rest_framework.request import Request
import logging
from common.models.akas import AccessKeyAndSecretModel

logger = logging.getLogger(__name__)

class HasAccessKeyVerifySignaturePermission(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request: Request, view):
        
        authorization = request._request.headers.get("Authorization", "")
  
       
        if not authorization:
            logger.warning(f"{request._request.path} has no Authorization header from {request._request.META.get('REMOTE_ADDR', '')}")
            return False
        
        log = {
            "path": request._request.path,
            "authorization": authorization,
            "remote_addr": request._request.META.get("REMOTE_ADDR", ""),
            "verify_result": False,
        }
        key, _ = authorization.split(" ")
        obj: AccessKeyAndSecretModel = AccessKeyAndSecretModel.objects.get(key=key)
        verify_res= obj.verify_signature(request)
        log["verify_result"] = verify_res
        if not verify_res:
            logger.warning(log)
        else:
            logger.info(log)
        return verify_res

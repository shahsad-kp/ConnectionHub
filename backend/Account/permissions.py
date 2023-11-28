from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsVerified(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user:
            return False
        return request.user.is_verified

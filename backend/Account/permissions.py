from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsVerified(BasePermission):
    def __init__(self):
        self.message = None

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user:
            return False
        if not request.user.is_verified:
            self.message = 'Your email isn\'t verified'
            return False
        return True


class NotVerified(BasePermission):
    def __init__(self):
        self.message = None

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not request.user:
            return False
        if request.user.is_verified:
            self.message = 'Your email already verified.'
            return False
        return True

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from Account.models import User


class ProfileAPIPermission(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        user: 'User' = request.user
        try:
            _ = user.profile
            return request.method in ['GET', 'PUT', 'PATCH']
        except ObjectDoesNotExist:
            return request.method == 'POST'

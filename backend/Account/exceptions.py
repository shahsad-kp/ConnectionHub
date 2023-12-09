from rest_framework import status
from rest_framework.exceptions import APIException


class TokenExpired(APIException):
    default_detail = 'Token Expired'
    default_code = 'token_expired'
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidToken(APIException):
    default_detail = 'Invalid Token'
    default_code = 'invalid_token'
    status_code = status.HTTP_403_FORBIDDEN

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework import authentication

from main.services import extract_token_from_request, verify_token


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token_string = extract_token_from_request(request)
        if token_string is None:
            return None
        user = verify_token(token_string, request)
        if user is None:
            raise Exception('Неправильный токен.')
        return user, token_string


class JWTScheme(OpenApiAuthenticationExtension):
    target_class = "main.authentication.CustomAuthentication"  # full import path OR class ref
    name = "JWTAuthentication"  # custom name for your auth scheme

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Token value'
        }

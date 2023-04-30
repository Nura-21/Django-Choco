import json
from datetime import datetime

import jwt
from django.conf import settings

from main.models import MainUser


def create_token(user, request):
    payload = {
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'credit_cards': json.dumps(
            list(user.creditcard_set.values()),
            default=str
        ),
        'bonuses': user.bonuses,
        'sign_timestamp': datetime.now().timestamp(),
    }
    token = jwt.encode(payload, settings.JWT_KEY, algorithm='HS256')
    return token


def verify_user(request, email, password):
    user = MainUser.objects.filter(email=email)
    if not user.exists():
        raise Exception('Пользователя с таким email не существует')
    user = user.first()
    if not user.check_password(password):
        raise Exception('Неверный пароль')
    token = create_token(user, request)
    return token


def extract_token_from_request(request):
    header_names = ['Auth-Token', 'HTTP_AUTH_TOKEN', 'AUTH_TOKEN', 'Authorization']
    token_string = None
    for header_name in header_names:
        if header_name in request.headers and len(request.headers[header_name]) != 0:
            token_string = request.headers[header_name]
    return token_string


def verify_token(token_string, request):

    payload = jwt.decode(token_string, settings.JWT_KEY, algorithms=['HS256'])
    user_id = payload['user_id']
    user = MainUser.objects.filter(id=user_id)
    if not user.exists():
        return None
    return user.first()

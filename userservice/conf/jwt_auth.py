import jwt
from datetime import datetime, timedelta
from django.conf import settings

def GenerateAccessToken(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'mobile': user.mobile,
        'full_name': user.full_name,
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.ACCESS_SECRET_KEY, algorithm='HS256')
    return token

def GenerateRefreshToken(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(days=30),
        'iat': datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.REFRESH_SECRET_KEY, algorithm='HS256')
    return token


def DecodeAccessToken(token):
    try:
        payload = jwt.decode(token, settings.ACCESS_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    

def DecodeRefreshToken(token):
    try:
        payload = jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
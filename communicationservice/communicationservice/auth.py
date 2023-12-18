from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.core.cache import cache
from conf.jwt_auth import DecodeAccessToken
from api.models import UserMaster
from rest_framework import status

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization', '')
        
        if not authorization_header.startswith('Bearer '):
            return None

        token = authorization_header.split(' ')[1]
        payload = DecodeAccessToken(token)
        if not payload:
            return None

        user_id = payload.get('user_id')
        user = cache.get(f'user_{user_id}')

        if user is None:
            try:
                user = UserMaster.objects.select_related('branch').get(pk=user_id)
                if not user.is_active:
                    raise AuthenticationFailed('User is not active', code='user_inactive')
            except UserMaster.DoesNotExist:
                raise AuthenticationFailed('User not found', code='user_not_found')

            # Cache the user
            cache.set(f'user_{user_id}', user)

        return user, None

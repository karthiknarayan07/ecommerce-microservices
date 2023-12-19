from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from conf.jwt_auth import DecodeAccessToken
from api.models import UserMaster

from conf.redis_conn import GetModelObject,SetModelObject



class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization', '')
        
        if not authorization_header.startswith('Bearer '):
            return None

        token = authorization_header.split(' ')[1]
        payload = DecodeAccessToken(token)
        if payload is None:
            raise AuthenticationFailed('Authentication failed. Token is either invalid or expired.', code='token_invalid_or_expired')

        user_id = payload.get('user_id')
        user = GetModelObject(f'user_{user_id}')

        if user is None:
            try:
                user = UserMaster.objects.get(pk=user_id)
                if not user.is_active:
                    raise AuthenticationFailed('User is not active', code='user_inactive')
            except UserMaster.DoesNotExist:
                raise AuthenticationFailed('User not found', code='user_not_found')

            # Caching the user for 12 hours (720 minutes)
            SetModelObject(f'user_{user_id}', user, ttl=720 * 60)

        return user, None

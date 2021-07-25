from rest_framework.authentication import get_authorization_header, BaseAuthentication
from rest_framework import exceptions

from api.models import User
import jwt
from rest_framework import authentication
from django.conf import settings


# implementing a JWT-based authentication solution
class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        if not auth_data:
            return None
        prefix, token = auth_data.decode('utf-8').split(' ')

        try:
            # decoding jwt token
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithm="HS256", options={"verify_signature": False})
            username = payload['username']
            user = User.objects.get(username=username)
            return user, token
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token is expired, Login again')
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Token is invalid')
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed('No such user')

        return super().authenticate(request)

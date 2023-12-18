from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password

from django.core.cache import cache
import redis

from conf.jwt_auth import GenerateAccessToken,GenerateRefreshToken

from conf.rabbit_sender import rabbitconnection



# Create your views here.

class CustomResponse():
    def successResponse(self, data, status=status.HTTP_200_OK, total=0, description="SUCCESS"):
        return Response(
            {
                "success": True,
                "errorCode": 0,
                "description": description,
                "total": total,
                "info": data
            }, status=status)

    def errorResponse(self, data={}, description="ERROR", errorCode=1, status=status.HTTP_200_OK):
        return Response(
            {
                "success": False,
                "errorCode": errorCode,
                "description": description,
                "info": data
            }, status=status)


class TestView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        print("i am being called test api")
        try:
            # value = cache.get('pesto')
            value=78965
            resp ={
                'message': 'Hello World user service',
                'cache':value
            }
            return CustomResponse().successResponse(data=resp)
        except Exception as error:
            return CustomResponse().errorResponse(data=str(error))
        
        


class LoginView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self,request):
        try:
            
            mobile = request.data.get('mobile')
            password = request.data.get('password')
            
            if not mobile or not password:
                return CustomResponse().errorResponse(description="mobile and password are required")
            
            user = UserMaster.objects.filter(mobile=mobile).first()
            
            if user and check_password(password, user.password):
                refresh_token = GenerateRefreshToken(user)
                access_token = GenerateAccessToken(user)
                data = {
                    'refresh_token':str(refresh_token),
                    'access_token':str(access_token)
                }
                
                # save refresh token in user tokens table
                return CustomResponse().successResponse(data=data)
            
            response = {
                'status':"invalid login details"
            }
            return CustomResponse().errorResponse(data=response)
        
        except Exception as error:
            return CustomResponse().errorResponse(data=str(error))
        
        
        
class RegisterView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self,request):
        try:
            
            mobile = request.data.get('mobile')
            password = request.data.get('password')
            
            if not mobile or not password:
                return CustomResponse().errorResponse(description="mobile and password are required to login")
            
            user = UserMaster(mobile=mobile,password=make_password(password))
            user.custom_permissions = ['is_enduser']
            user.save()
            
            if user:
                refresh_token = GenerateRefreshToken(user)
                access_token = GenerateAccessToken(user)
                data = {
                    'refresh_token':str(refresh_token),
                    'access_token':str(access_token)
                }
                payload = {
                    'identifier': '1',
                    'user_id': user.pk,
                    'mobile': mobile,
                }
                rabbitconnection(message=payload, queue='user_queue')
                # save refresh token in user tokens table
                return CustomResponse().successResponse(data=data)
            
            response = {
                'status':"invalid login details"
            }
            return CustomResponse().errorResponse(data=response)
        
        except Exception as error:
            return CustomResponse().errorResponse(data=str(error))
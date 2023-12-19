from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated

from .models import *
from django.contrib.auth.hashers import make_password, check_password

from conf.jwt_auth import GenerateAccessToken,GenerateRefreshToken

from conf.rabbit_sender import RabbitSingleton

from django.views.decorators.cache import never_cache




# Create your views here.
# using same response structure for all apis - keeping frontend in mind

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
        
        
class RegisterView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self,request):
        try:
            # get details from request object
            mobile = request.data.get('mobile',None)
            email = request.data.get('email',None)
            full_name = request.data.get('full_name',None)
            password = request.data.get('password',None)
            
            if not mobile or not password or not email or not full_name:
                return CustomResponse().errorResponse(description="please enter all the details")
            
            # creae user in usermaster table with role and permissions
            # hashing the passowrd before saving in db
            
            # we can you use serializer to validate the data but for now i am avoiding to reduce complexity
            
            user = UserMaster()
            user.mobile = mobile
            user.email = email
            user.full_name = full_name
            user.password = make_password(password)
            user.custom_permissions = ['is_enduser',]
            user.save()
            
            # after saving user in usermaster table, generate refresh token and access token
            if user:
                refresh_token = GenerateRefreshToken(user)
                access_token = GenerateAccessToken(user)
                data = {
                    'refresh_token':str(refresh_token),
                    'access_token':str(access_token)
                }
                # sending message to rabbitmq queue to send signup email to user with offers,coupons etc if needed
                payload = {
                    'identifier': '1',
                    'user_id': user.pk,
                    'mobile': mobile,
                    'email': email,
                    'full_name': full_name,
                }
                rabbit = RabbitSingleton()
                rabbit.send_message(payload, queue='communication_queue')
                
                # return response with tokens
                return CustomResponse().successResponse(data=data)
            
            # include more cases to handle errors like duplicate mobile number, email etc
        except Exception as error:
            return CustomResponse().errorResponse(data=str(error))
        
        

class SuperAdminRegisterView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self,request):
        try:
            # get details from request object
            mobile = request.data.get('mobile',None)
            email = request.data.get('email',None)
            full_name = request.data.get('full_name',None)
            password = request.data.get('password',None)
            
            if not mobile or not password or not email or not full_name:
                return CustomResponse().errorResponse(description="please enter all the details")
            
            # creae user in usermaster table with role and permissions
            # hashing the passowrd before saving in db
            
            # we can you use serializer to validate the data but for now i am avoiding to reduce complexity
            
            user = UserMaster()
            user.mobile = mobile
            user.email = email
            user.full_name = full_name
            user.password = make_password(password)
            user.role = 'SUPERADMIN'
            user.custom_permissions = ['is_enduser','is_superadmin',]
            user.save()
            
            # after saving user in usermaster table, generate refresh token and access token
            if user:
                refresh_token = GenerateRefreshToken(user)
                access_token = GenerateAccessToken(user)
                data = {
                    'refresh_token':str(refresh_token),
                    'access_token':str(access_token)
                }
                # sending message to rabbitmq queue to send signup email to user with offers,coupons etc if needed
                payload = {
                    'identifier': '1',
                    'user_id': user.pk,
                    'mobile': mobile,
                    'email': email,
                    'full_name': full_name,
                }
                rabbit = RabbitSingleton()
                rabbit.send_message(payload, queue='communication_queue')
                
                # return response with tokens
                return CustomResponse().successResponse(data=data)
            
            # include more cases to handle errors like duplicate mobile number, email etc
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
            
            # checking password against the hashed password in db
            if user and check_password(password, user.password):
                refresh_token = GenerateRefreshToken(user)
                access_token = GenerateAccessToken(user)
                data = {
                    'refresh_token':str(refresh_token),
                    'access_token':str(access_token)
                }
                
                # save refresh token in user tokens table if needed
                return CustomResponse().successResponse(data=data)
            response = {
                'status':"invalid login details"
            }
            return CustomResponse().errorResponse(data=response,description="invalid login details")
        
        except Exception as error:
            return CustomResponse().errorResponse(data=str(error))
        
        
class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        try:
            # get user from request object - cache first and then db - implemenented redis cache
            print(request.headers)
            print("i am profile api")
            user = request.user
            if user:
                data = {
                    'mobile':user.mobile,
                    'email':user.email,
                    'full_name':user.full_name,
                }
                return CustomResponse().successResponse(data=data)
            return CustomResponse().errorResponse(description="user not found")
        except Exception as error:
            return CustomResponse().errorResponse(data=str(error))
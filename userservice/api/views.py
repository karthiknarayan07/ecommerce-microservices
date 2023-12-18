from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from django.db import transaction
from django.contrib.auth.hashers import make_password, check_password

from django.core.cache import cache
import redis




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
            value = cache.get('pesto')
            resp ={
                'message': 'Hello World user service',
                'cache':value
            }
            return CustomResponse().successResponse(data=resp)
        except Exception as error:
            return CustomResponse().errorResponse(data=str(error))
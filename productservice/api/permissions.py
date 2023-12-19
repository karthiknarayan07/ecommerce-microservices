from rest_framework import status
from rest_framework.response import Response

from django.conf import settings

import requests

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



def custom_method_permissions(required_permissions):
    def decorator(view_method):
        def wrapped_view(self, request, *args, **kwargs):
            # chechking required permissions
            
            authorization_header = request.headers.get('Authorization',None)
            if not authorization_header:
                return CustomResponse().errorResponse(description="Authorization header missing", errorCode=1,)
            
            headers = {'Authorization': authorization_header, 'Content-Type': 'application/json'}

            # call auth service to check permissions
            try:
                response = requests.get(settings.AUTH_SERVICE_URL, headers=headers)
                if response.status_code == 200 and response.json().get('success',False):
                    data = response.json().get('info',{})
                    permissions = data.get('permissions',[])
                    role = data.get('role',None)
                    
                    # attach user data to request object
                    request.user_data = data
                    
                    # checking permsissions from auth service
                    if not all(permission in permissions for permission in required_permissions):
                        return CustomResponse().errorResponse(description="You dont have permission for this operation", errorCode=1,)
            except Exception as e:
                return CustomResponse().errorResponse(description=f"Error while checking permissions for auth service:- {str(e)}", errorCode=1,)
            
            # if all permissions are there, then call the view method
            return view_method(self, request, *args, **kwargs)

        return wrapped_view

    return decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated



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


# for this view we can add extra permissions so that only accessibile to internal services not end user
# for now we are allowing any user to access this api later hide this url
# from nginx and add permissions to access from other microservices

class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request):
        try:
            # get user from request object - cache first and then db - implemenented redis cache
            # i am using same user token we can implement API token for internal services to reduce token payload from request
            user = request.user
            if user:
                data = {
                    'mobile':user.mobile,
                    'email':user.email,
                    'full_name':user.full_name,
                    'permissions':user.custom_permissions,
                    'role':user.role,
                }
                return CustomResponse().successResponse(data=data)
            return CustomResponse().errorResponse(description="user not found - clear token in FE and logout")
        except Exception as error:
            return CustomResponse().errorResponse(data=str(error))
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.models import *
from api.serializers import *

from api.permissions import custom_method_permissions

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


class OrdersView(APIView):
    permission_classes = (AllowAny,)
    
    @custom_method_permissions(['is_enduser'])
    def get(self, request):
        try:
            orders = Orders.objects.filter(mobile=request.user_data.get('mobile'))
            serializer = OrdersSerializer(orders, many=True)
            return CustomResponse().successResponse(data=serializer.data)
        except Exception as error:
            return CustomResponse().errorResponse(description=str(error))
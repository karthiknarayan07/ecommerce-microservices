from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.db import transaction

from api.models import *
from api.serializers import *

from conf.rabbit_sender import RabbitSingleton

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
    
    # this view should be protected by service to service authentication so that only product service can call this api
    # we can implement API key based authentication
    
    @transaction.atomic
    def post(self, request):
        try:
            # get data from POST body
            data = request.data
            product = data.get('product')
            user_data = data.get('user_data')
            
            order  = Orders()
            order.name = product.get('name')
            order.mobile = user_data.get('mobile')
            order.price = product.get('price')
            order.quantity = data.get('quantity')
            order.status = 'CREATED'
            order.created_by = user_data.get('mobile')
            order.save()
            
            serializer = OrdersSerializer(order)
            
            # send order confirmation email to user - rabbitmq
            payload = {
                'identifier': '2',
                'order': serializer.data,
                'email': user_data['email'],
                'product': product
            }
            rabbit = RabbitSingleton()
            rabbit.send_message(message=payload, queue='communication_queue')
            
            return CustomResponse().successResponse(data=serializer.data)            
        except Exception as error:
            transaction.set_rollback(True)
            return CustomResponse().errorResponse(description=str(error))
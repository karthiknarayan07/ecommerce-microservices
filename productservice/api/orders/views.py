from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.models import *
from api.serializers import *


from django.db import transaction
from django.db import transaction
from django.conf import settings

from api.permissions import custom_method_permissions

import requests
import json


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
    @transaction.atomic
    def post(self, request):
        try:
            # get data from POST body
            data = request.data
            
            product_id = data.get('product_id',None)
            quantity = int(data.get('quantity',0))
            
            # applying pessimistic lock on record
            product_obj = Products.objects.select_for_update().filter(id=product_id).first()
            if product_obj:
                if product_obj.stock_quantity < quantity:
                    return CustomResponse().errorResponse(description="Insufficient stock")
                
                # serialize to send to orderservice API
                product_serializer = ProductsSerializer(product_obj)
                
                if quantity > 0:
                    # decrese the stock quantity
                    product_obj.stock_quantity = product_obj.stock_quantity - quantity
                    product_obj.save()
                    
                    # create order by calling orderservice API
                    response = self.CreateOrder(request,product_serializer.data,quantity)
                    
                    if response.status_code == 200 and response.json().get('success',False):
                        data = response.json().get('info',{})
                        resp = {
                            'status':'order created successfully',
                            'order_id': data.get('id',None),
                            'product_name': product_obj.name,
                            'product_price': product_obj.price,
                            'quantity': quantity,
                        }
                        return CustomResponse().successResponse(data=resp)
                    
                    # api designed to return 200 even if order is not created if not 200 then return error
                    if response.status_code != 200:
                        # order service is down - we can write alerting and monitoring code here to notify devops team or send email to them
                        return CustomResponse().errorResponse(description="Error while creating order - order service down")
                    else:
                        # order service is up but order is not created
                        return CustomResponse().errorResponse(description="Error while creating order")
                    
                return CustomResponse().errorResponse(description="Quantity should be greater than 0")                    
            return CustomResponse().errorResponse(description="Product not found")
        except Exception as error:
            transaction.set_rollback(True)
            return CustomResponse().errorResponse(description=str(error))
        
        
    
    def CreateOrder(self,request,product,quantity):
        headers = {'Authorization': request.headers.get('Authorization',None), 'Content-Type': 'application/json'}
        payload = {'product': product, 'quantity': quantity, 'user_data': request.user_data}
        response = requests.post(settings.ORDER_SERVICE_URL+'orders', headers=headers, data=json.dumps(payload))
        return response
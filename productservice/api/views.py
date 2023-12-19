from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated

from .models import *
from .serializers import *

from conf.rabbit_sender import RabbitSingleton
from .permissions import custom_method_permissions

from django.db import transaction
from django.core.cache import cache




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


class ProductsView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self,request):
        try:
            # get data from GET query params
            product_id = request.GET.get('product_id',None)
            
            # if product_id is present then get data from db
            if product_id:
                # first check in redis cache
                product_data = cache.get('products_'+str(product_id))
                
                if product_data:
                    return CustomResponse().successResponse(data=product_data)
                
                # if not present in redis cache then get from db
                product_obj = Products.objects.filter(product_id=product_id).first()
                
                if product_obj:
                    serializer = ProductsSerializer(product_obj)
                    
                    # now will save in redis cache for faster access later in GET api
                    cache.set('products_'+str(product_id), serializer.data, timeout=700*60)
                    
                    return CustomResponse().successResponse(data=serializer.data)
                
                return CustomResponse().errorResponse(description="Product not found")
            
            # if product_id is not present then get all products data from db
            products_obj = Products.objects.all()
            serializer = ProductsSerializer(products_obj, many=True)
            return CustomResponse().successResponse(data=serializer.data)
        except Exception as error:
            return CustomResponse().errorResponse(description=str(error))
    
    @custom_method_permissions(['is_superadmin'])
    @transaction.atomic
    def post(self, request):
        try:
            # get data from POST body
            data = request.data
            
            # serialize FE data
            serializer = ProductsSerializer(data=data)
            
            # if valid data, save to db
            if serializer.is_valid():
                prod_obj = serializer.save() # save to db
                
                # now will save in redis cache for faster access later in GET api
                cache.set('products_'+str(prod_obj.pk), serializer.data, timeout=700*60)
                
                # return saved product details to FE
                return CustomResponse().successResponse(data=serializer.data)
            
            # if errors should handled individually and separately then we can, write different conditions in try except blocks
            # of serializer.errors and return different error messages with error codes
            return CustomResponse().errorResponse(serializer.errors)
        except Exception as error:
            transaction.set_rollback(True)
            return CustomResponse().errorResponse(description=str(error))
        
    
    @custom_method_permissions(['is_superadmin'])
    @transaction.atomic
    def put(self, request):
        try:
            # get data from POST body
            data = request.data
            
            # existing product object
            product_obj = Products.objects.filter(product_id=data['product_id']).first()
            
            if product_obj:
                # validating new data, allowing partial update
                serializer = ProductsSerializer(product_obj, data=data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return CustomResponse().successResponse(data=serializer.data)
                return CustomResponse().errorResponse(data=serializer.errors)
            
            # if each error needs to be handled separately then we can, write different conditions in try except blocks
            # of serializer.errors and return different error messages with error codes
            return CustomResponse().errorResponse(serializer.errors)
        except Exception as error:
            transaction.set_rollback(True)
            return CustomResponse().errorResponse(description=str(error))
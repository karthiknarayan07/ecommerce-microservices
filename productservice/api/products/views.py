from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.models import *
from api.serializers import *

from api.permissions import custom_method_permissions

from django.db import transaction
from django.db import transaction, IntegrityError

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
                # get from db
                product_obj = Products.objects.filter(id=product_id).first()
                if product_obj:
                    serializer = ProductsSerializer(product_obj)
                    
                    # save in redis cache for faster access later in GET api
                    cache.set('products_'+str(product_obj.pk), serializer.data, timeout=700*60)
                    
                    return CustomResponse().successResponse(data=serializer.data)
                # no record with id
                return CustomResponse().errorResponse(description="Product not found")
            # give product id in query params
            return CustomResponse().errorResponse(description="please enter product id")
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
                
                # invalidate redis cache
                cache.delete('products_'+str(prod_obj.pk))
                cache.delete('products')
                
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
            
            # applying pessimistic lock so that no other user can update same record at same time else it will throw integrity error
            product_obj = Products.objects.select_for_update().filter(id=data['product_id']).first()
            
            if product_obj:
                # validating new data, allowing partial update
                serializer = ProductsSerializer(product_obj, data=data, partial=True, context={'request': request})
                if serializer.is_valid():
                    product_obj = serializer.save()
                    
                    # invalidate redis cache
                    cache.delete('products_'+str(product_obj.pk))
                    cache.delete('products')
                    
                    return CustomResponse().successResponse(data=serializer.data)
                return CustomResponse().errorResponse(data=serializer.errors)
            return CustomResponse().errorResponse(description="Product not found.")

        except IntegrityError:
            transaction.set_rollback(True)
            return CustomResponse().errorResponse(description="Concurrent update conflict. Try again.")

        except Exception as error:
            transaction.set_rollback(True)
            return CustomResponse().errorResponse(description=str(error))
        
        
        
class ReadProductsView(APIView):
    permission_classes = (AllowAny,)
    
    def get(self,request):
        try:
            # pagination and query params not implemented due to time constraint 
            
            # first check in redis cache - cache hit
            product_data = cache.get('products')
            if product_data:
                return CustomResponse().successResponse(data=product_data)
            
            # if not present in redis cache then get from db - cache miss
            products = Products.objects.filter()
            
            if products:
                serializer = ProductsSerializer(products,many=True)
                
                # now will save in redis cache for faster access later in GET api
                cache.set('products', serializer.data, timeout=700*60)
                
                return CustomResponse().successResponse(data=serializer.data)
            
            return CustomResponse().errorResponse(description="Products not found")
        except Exception as error:
            return CustomResponse().errorResponse(description=str(error))
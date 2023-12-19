from rest_framework import serializers
from django.apps import apps

from .models import *

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
from rest_framework import serializers
from django.apps import apps

from .models import *

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'
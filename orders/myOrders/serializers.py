from rest_framework import serializers
from .models import Customer, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'phone_number']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'item', 'amount', 'time', 'customer']

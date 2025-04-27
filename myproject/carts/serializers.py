from rest_framework import serializers
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'tree', 'quantity', 'get_total_price']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'is_active', 'created_at', 'updated_at', 'cart_items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()

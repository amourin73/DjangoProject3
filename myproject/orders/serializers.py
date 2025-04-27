from rest_framework import serializers
from .models import Order, OrderItem
from ..trees.models import Tree
from ..trees.serializers import TreeSerializer

from trees.models import Tree

class OrderItemSerializer(serializers.ModelSerializer):
    tree = TreeSerializer(read_only=True)
    tree_id = serializers.PrimaryKeyRelatedField(
        queryset=Tree.objects.all(),
        source='tree',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'tree', 'tree_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'total_price', 'status', 'items']
        read_only_fields = ['user', 'total_price', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=self.context['request'].user, **validated_data)

        total_price = 0
        for item_data in items_data:
            tree = item_data['tree']
            quantity = item_data['quantity']
            price = tree.price

            OrderItem.objects.create(
                order=order,
                tree=tree,
                quantity=quantity,
                price=price
            )

            tree.available_quantity -= quantity
            tree.save()
            total_price += price * quantity

        order.total_price = total_price
        order.save()
        return order

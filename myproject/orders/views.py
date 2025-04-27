from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from ..carts.models import Cart, CartItem


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(detail=False, methods=['POST'])
    def create_from_cart(self, request):
        try:
            cart = Cart.objects.get(user=request.user, is_active=True)
        except Cart.DoesNotExist:
            return Response({'error': 'Active cart not found.'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = CartItem.objects.filter(cart=cart)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        order_data = {
            'items': [
                {'tree_id': item.tree.id, 'quantity': item.quantity}
                for item in cart_items
            ]
        }

        serializer = self.get_serializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()
            cart_items.delete()
            cart.is_active = False
            cart.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet:
    pass
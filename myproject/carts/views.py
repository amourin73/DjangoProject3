from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def my_cart(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        serializer = CartItemSerializer(data=request.data)

        if serializer.is_valid():
            tree = serializer.validated_data['tree']
            quantity = serializer.validated_data.get('quantity', 1)

            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                tree=tree,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def remove_item(self, request):
        cart = Cart.objects.get(user=request.user, is_active=True)
        tree_id = request.data.get('tree_id')

        try:
            cart_item = CartItem.objects.get(cart=cart, tree_id=tree_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not in cart'}, status=status.HTTP_404_NOT_FOUND)

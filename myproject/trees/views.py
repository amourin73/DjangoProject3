# trees/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tree, TreeRating
from .serializers import TreeSerializer, TreeRatingSerializer

class IsSellerOrAdmin:
    pass

class TreeViewSet(viewsets.ModelViewSet):
    queryset = Tree.objects.all()
    serializer_class = TreeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'seller', 'price']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsSellerOrAdmin()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def rate_tree(self, request, pk=None):
        tree = self.get_object()
        serializer = TreeRatingSerializer(data=request.data)

        if serializer.is_valid():
            # Check if user already rated this tree
            existing_rating = TreeRating.objects.filter(
                tree=tree,
                user=request.user
            ).first()

            if existing_rating:
                serializer.update(existing_rating, serializer.validated_data)
            else:
                serializer.save(tree=tree, user=request.user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

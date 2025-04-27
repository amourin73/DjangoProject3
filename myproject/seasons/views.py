from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Season, SeasonalRecommendation
from .serializers import SeasonalRecommendationSerializer
from datetime import datetime

class SeasonalRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SeasonalRecommendation.objects.filter(is_active=True)
    serializer_class = SeasonalRecommendationSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['GET'])
    def current_season_recommendations(self, request):
        current_month = datetime.now().month

        try:
            # Find the current season based on month
            current_season = Season.objects.get(
                start_month__lte=current_month,
                end_month__gte=current_month
            )
            recommendations = SeasonalRecommendation.objects.filter(
                season=current_season,
                is_active=True
            ).first()

            if recommendations:
                serializer = self.get_serializer(recommendations)
                return Response(serializer.data)
            else:
                return Response({'message': 'No recommendations for the current season.'}, status=404)

        except Season.DoesNotExist:
            return Response({'message': 'Unable to determine current season.'}, status=404)

from rest_framework import serializers
from .models import Season, SeasonalRecommendation
from ..trees.serializers import TreeSerializer


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'

class SeasonalRecommendationSerializer(serializers.ModelSerializer):
    trees = TreeSerializer(many=True, read_only=True)
    season = SeasonSerializer(read_only=True)

    class Meta:
        model = SeasonalRecommendation
        fields = '__all__'

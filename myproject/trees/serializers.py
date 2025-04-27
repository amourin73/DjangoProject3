# trees/serializers.py
from rest_framework import serializers

from . import models
from .models import Tree, TreeRating, TreeCategory
from accounts.models import CustomUser  # Absolute import fixed here

class TreeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeCategory
        fields = '__all__'

class TreeSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    total_ratings = serializers.SerializerMethodField()
    category = TreeCategorySerializer(read_only=True)

    class Meta:
        model = Tree
        fields = '__all__'

    def get_average_rating(self, obj):
        ratings = obj.ratings.all()
        return round(ratings.aggregate(models.Avg('rating'))['rating__avg'] or 0, 2)

    def get_total_ratings(self, obj):
        return obj.ratings.count()

class TreeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeRating
        fields = '__all__'
        read_only_fields = ['user']

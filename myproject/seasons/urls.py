from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SeasonalRecommendationViewSet

router = DefaultRouter()
router.register(r'seasonal-recommendations', SeasonalRecommendationViewSet, basename='seasonal-recommendation')

urlpatterns = [
    path('', include(router.urls)),
]

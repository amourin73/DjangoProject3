from django.db import models

# Create your models here.
from django.db import models
# from trees.models import Tree

class Season(models.Model):
    SEASON_CHOICES = (
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
    )

    name = models.CharField(max_length=10, choices=SEASON_CHOICES, unique=True)
    start_month = models.PositiveIntegerField()  # 1-12
    end_month = models.PositiveIntegerField()    # 1-12

    def __str__(self):
        return self.name

class SeasonalRecommendation(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    # trees = models.ManyToManyField(Tree, related_name='seasonal_recommendations')

    title = models.CharField(max_length=200)
    description = models.TextField()
    climate_suitability = models.TextField(blank=True)
    planting_tips = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.season.name} Recommendations"

# trees/models.py
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models
from accounts.models import CustomUser  # Absolute import fixed here

class TreeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Tree(models.Model):
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(TreeCategory, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'seller'})

    # Pricing and Inventory
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_quantity = models.PositiveIntegerField(default=0)

    # Tree Specifics
    age = models.PositiveIntegerField()
    height = models.FloatField()  # in meters
    description = models.TextField()

    # Images
    main_image = models.ImageField(upload_to='tree_images/', null=True)
    additional_images = models.ManyToManyField('TreeImage', blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TreeImage(models.Model):
    image = models.ImageField(upload_to='tree_images/')
    description = models.CharField(max_length=200, blank=True)

class TreeRating(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tree', 'user')

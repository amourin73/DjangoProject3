from django.db import models

# from myproject.trees.models import Tree


# from users.models import CustomUser
# from trees.models import Tree

class Cart(models.Model):
    # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.cartitem_set.all())

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.tree.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.tree.name}"

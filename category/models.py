from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    category = models.CharField(max_length=50)
    product_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name

class FavoriteProduct(models.Model):
    user_id = models.IntegerField()  # Changed from ForeignKey to IntegerField
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'product')

    def __str__(self):
        return f"User {self.user_id}'s favorite: {self.product.name}"

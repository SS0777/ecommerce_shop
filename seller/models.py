# seller/models.py
from django.db import models
from accounts.models import User

class SellerStats(models.Model):
    seller = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_stats')
    total_products = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    monthly_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '판매자 통계'
        verbose_name_plural = '판매자 통계'

    def __str__(self):
        return f"{self.seller.username}의 판매 통계"

class Product(models.Model):
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.SELLER}
    )
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    seller = models.ForeignKey(User, related_name='seller_orders', on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.product_name} ({self.status})"
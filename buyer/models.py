# buyer/models.py
from django.db import models
from accounts.models import User
from seller.models import Product

class BuyerStats(models.Model):
    buyer = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer_stats')
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_purchase_date = models.DateTimeField(null=True, blank=True)
    favorite_categories = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '구매자 통계'
        verbose_name_plural = '구매자 통계'

    def __str__(self):
        return f"{self.buyer.username}의 구매 통계"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', '주문 대기'),
        ('PAID', '결제 완료'),
        ('SHIPPING', '배송 중'),
        ('DELIVERED', '배송 완료'),
        ('CANCELLED', '주문 취소')
    ]
    
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': User.BUYER}
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.buyer.username}의 주문 - {self.product.name}"
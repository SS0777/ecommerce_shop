from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DailySales(models.Model):
    date = models.DateField(unique=True)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    order_count = models.PositiveIntegerField()
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    
class Settlement(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2)
    commission = models.DecimalField(max_digits=12, decimal_places=2)
    settlement_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
# models.py

from django.db import models
from django.apps import apps  # 순환 임포트 문제를 피하기 위한 apps 모듈 임포트

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, 
                               on_delete=models.CASCADE, related_name='children')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)  # null=False로 수정

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)  # max_digits를 12로 늘림
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    additional_images = models.ManyToManyField(
        'ProductImage',
        related_name='products_as_additional',
        blank=True
    )
    likes = models.ManyToManyField('accounts.User', related_name='liked_products')  # 순환 임포트를 피하기 위해 'accounts.User'로 문자열 사용
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 인기 제품을 위한 popularity 필드 (좋아요 수를 기준으로)
    popularity = models.PositiveIntegerField(default=0)

    def is_new_product(self):
        """
        제품이 등록된 지 7일 이내인지 확인
        """
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at >= (timezone.now() - timedelta(days=7))

    def update_popularity(self):
        """ 제품의 인기 점수(좋아요 수)를 업데이트하는 메서드 """
        self.popularity = self.likes.count()
        self.save()

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    image = models.ImageField(upload_to='products/additional/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

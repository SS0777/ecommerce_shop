from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product

User = get_user_model()

class Review(models.Model):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='reviews'  # Product에서 reviews로 접근 가능하도록 추가
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='product_reviews'  # User의 다른 리뷰들과 구분
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=[(i, f"{'★' * i}{'☆' * (5-i)}") for i in range(1, 6)]  # 별표로 표시
    )
    content = models.TextField(
        verbose_name='리뷰 내용',
        help_text='제품에 대한 리뷰를 작성해주세요.'
    )
    likes = models.ManyToManyField(
        User, 
        related_name='liked_reviews',
        blank=True  # 좋아요가 없을 수 있음
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # 최신 리뷰가 먼저 보이도록
        verbose_name = '리뷰'
        verbose_name_plural = '리뷰들'
        # 한 사용자가 같은 제품에 대해 여러 리뷰를 작성하지 못하도록
        unique_together = ['user', 'product']

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"

    @property
    def image_count(self):
        return self.images.count()

class ReviewImage(models.Model):
    review = models.ForeignKey(
        Review, 
        related_name='images', 
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='review_images/%Y/%m/%d/',  # 날짜별로 폴더 구성
        verbose_name='리뷰 이미지'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '리뷰 이미지'
        verbose_name_plural = '리뷰 이미지들'
        ordering = ['created_at']

    def __str__(self):
        return f"Image for {self.review}"

class Report(models.Model):
    REPORT_TYPES = (
        ('spam', '스팸'),
        ('inappropriate', '부적절한 내용'),
        ('false_info', '허위 정보'),
        ('other', '기타'),
    )
    
    STATUS_CHOICES = (
        ('pending', '검토중'),
        ('resolved', '해결됨'),
        ('rejected', '반려됨'),
    )

    review = models.ForeignKey(
        Review, 
        on_delete=models.CASCADE,
        related_name='reports'
    )
    reporter = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='submitted_reports'
    )
    report_type = models.CharField(
        max_length=20, 
        choices=REPORT_TYPES,
        verbose_name='신고 유형'
    )
    description = models.TextField(
        verbose_name='신고 내용',
        help_text='구체적인 신고 사유를 작성해주세요.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='처리 상태'
    )

    class Meta:
        verbose_name = '신고'
        verbose_name_plural = '신고들'
        ordering = ['-created_at']
        # 같은 사용자가 같은 리뷰를 중복 신고하지 못하도록
        unique_together = ['review', 'reporter']

    def __str__(self):
        return f"Report on {self.review} by {self.reporter}"
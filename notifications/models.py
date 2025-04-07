from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('order', '주문 알림'),
        ('product', '상품 알림'),
        ('review', '리뷰 알림'),
        ('system', '시스템 알림'),
    )
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')  # 수신자
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)  # 알림 유형
    title = models.CharField(max_length=200)  # 제목
    message = models.TextField()  # 메시지 내용
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)  # 관련 객체의 ContentType
    object_id = models.PositiveIntegerField(null=True, blank=True)  # 관련 객체의 ID
    content_object = GenericForeignKey('content_type', 'object_id')  # GenericForeignKey를 사용해 객체와 연결
    is_read = models.BooleanField(default=False)  # 읽음 여부
    created_at = models.DateTimeField(auto_now_add=True)  # 알림 생성 시간 (자동으로 설정됨)

    def __str__(self):
        return f'{self.title} - {self.recipient.username}'

    class Meta:
        ordering = ['-created_at']  # 최근 알림부터 보여지도록 정렬

class EmailNotification(models.Model):
    STATUS_CHOICES = (
        ('pending', '대기중'),
        ('sent', '전송됨'),
        ('failed', '전송 실패'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 알림을 받을 사용자
    subject = models.CharField(max_length=200)  # 이메일 제목
    content = models.TextField()  # 이메일 내용
    sent_at = models.DateTimeField(null=True, blank=True)  # 이메일 발송 시간
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # 이메일 상태

    def __str__(self):
        return f'Email to {self.user.username}: {self.subject}'

    class Meta:
        ordering = ['-sent_at']  # 발송된 이메일을 최근 순으로 정렬

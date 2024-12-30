from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import re

# 사용자 모델 확장
class User(AbstractUser):
    # 사용자 유형에 대한 상수 선언
    BUYER = 'BUYER'
    SELLER = 'SELLER'
    
    USER_TYPE_CHOICES = [
        (BUYER, '구매자'),
        (SELLER, '판매자'),
    ]
    
    # user_type 필드
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES,
        default=BUYER  # 기본값으로 'BUYER' 설정
    )

    # 나머지 필드들
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    # 전화번호 유효성 검사
    def clean_phone_number(self):
        if self.phone_number:
            if not re.match(r'^[0-9]{10,15}$', self.phone_number):
                raise ValueError("전화번호는 10~15자리 숫자만 입력 가능합니다.")
        return self.phone_number

    # 저장 메서드
    def save(self, *args, **kwargs):
        self.clean_phone_number()  # 전화번호 유효성 검사
        super().save(*args, **kwargs)  # 부모 클래스의 save 호출


# 프로필 모델
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    grade = models.CharField(max_length=20, default='BRONZE')
    marketing_agree = models.BooleanField(default=False)

    business_number = models.CharField(max_length=20, null=True, blank=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    store_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Post_save 시그널로 Profile을 자동 생성하는 함수
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        """유저가 생성될 때 자동으로 프로필을 생성"""
        if created and not hasattr(instance, 'profile'):  # 중복 생성 방지
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        """유저가 저장될 때 프로필도 저장"""
        instance.profile.save()

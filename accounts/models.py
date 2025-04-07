from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps  # 순환 임포트 문제를 피하기 위한 apps 모듈 임포트

class User(AbstractUser):
    BUYER = 'BUYER'
    SELLER = 'SELLER'
    
    USER_TYPE_CHOICES = [
        (BUYER, '구매자'),
        (SELLER, '판매자'),
    ]
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES,
        default=BUYER
    )

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

    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    wishlist = models.ManyToManyField('products.Product', related_name='wishlist_users', blank=True)  # products.Product를 직접 import하지 않음

    def add_to_wishlist(self, product_id):
        # 순환 임포트 문제를 피하기 위해 apps.get_model을 사용하여 Product 모델 가져오기
        Product = apps.get_model('products', 'Product')
        product = Product.objects.get(id=product_id)
        self.wishlist.add(product)

    def remove_from_wishlist(self, product_id):
        Product = apps.get_model('products', 'Product')
        product = Product.objects.get(id=product_id)
        self.wishlist.remove(product)


    @property
    def is_seller(self):
        return self.user_type == self.SELLER

    @property
    def is_buyer(self):
        return self.user_type == self.BUYER
        
    def clean_phone_number(self):
        if self.phone_number:
            if not re.match(r'^[0-9]{10,15}$', self.phone_number):
                raise ValueError("전화번호는 10~15자리 숫자만 입력 가능합니다.")
        return self.phone_number

    def save(self, *args, **kwargs):
        self.clean_phone_number()
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    marketing_agree = models.BooleanField(default=False)
    
    # 새로 추가할 필드
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    
    # 판매자 전용 필드
    business_number = models.CharField(max_length=20, null=True, blank=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    store_description = models.TextField(null=True, blank=True)
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    store_grade = models.CharField(
        max_length=20, 
        choices=[
            ('BRONZE', '브론즈'),
            ('SILVER', '실버'),
            ('GOLD', '골드'),
            ('PLATINUM', '플래티넘')
        ],
        default='BRONZE'
    )
    
    # 구매자 전용 필드
    grade = models.CharField(
        max_length=20,
        choices=[
            ('BRONZE', '브론즈'),
            ('SILVER', '실버'),
            ('GOLD', '골드'),
            ('VIP', 'VIP')
        ],
        default='BRONZE'
    )
    shipping_address = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_grade_display(self):
        if self.user.is_seller:
            return dict(self._meta.get_field('store_grade').choices)[self.store_grade]
        return dict(self._meta.get_field('grade').choices)[self.grade]

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()
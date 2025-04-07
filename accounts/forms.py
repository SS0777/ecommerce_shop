from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Profile
from django.contrib.auth import authenticate

# 회원가입 폼
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    marketing_agree = forms.BooleanField(required=False)
    
    # 회원 유형 선택 필드
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        label='회원 유형',
        widget=forms.RadioSelect
    )
    
    # 판매자 추가 정보 필드
    business_number = forms.CharField(
        max_length=20, 
        required=False,
        label='사업자 등록번호'
    )
    store_name = forms.CharField(
        max_length=100, 
        required=False,
        label='상점명'
    )
    store_description = forms.CharField(
        widget=forms.Textarea, 
        required=False,
        label='상점 소개'
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2',
            'phone_number', 'address', 'marketing_agree',
            'user_type'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 판매자 필드에 클래스 추가
        self.fields['business_number'].widget.attrs['class'] = 'seller-field'
        self.fields['store_name'].widget.attrs['class'] = 'seller-field'
        self.fields['store_description'].widget.attrs['class'] = 'seller-field'

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        
        if user_type == 'SELLER':
            # 판매자인 경우 필수 필드 검증
            if not cleaned_data.get('business_number'):
                self.add_error('business_number', '판매자는 사업자 등록번호를 입력해야 합니다.')
            if not cleaned_data.get('store_name'):
                self.add_error('store_name', '판매자는 상점명을 입력해야 합니다.')
        
        return cleaned_data  # 이 return은 clean() 메소드 내에 있어야 합니다.

# 프로필 업데이트 폼
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_image', 'shipping_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # user 인스턴스가 존재하고 판매자인 경우에만 추가 필드 추가
        if self.instance and self.instance.user and self.instance.user.is_seller:
            self.fields['store_name'] = forms.CharField(required=False)
            self.fields['store_description'] = forms.CharField(widget=forms.Textarea, required=False)

# 사용자 정보 업데이트 폼
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 추가적인 커스터마이징, 예를 들어 사용자 유형에 따라 필드 수정 가능
        # 예시: self.fields['username'].widget.attrs['placeholder'] = '사용자 이름'
        
# 로그인 폼
class LoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        label='회원 유형',
        widget=forms.RadioSelect
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_type = self.cleaned_data.get('user_type')

        if username and password:
            # 사용자 이름과 유형으로 사용자 확인
            user = User.objects.filter(username=username, user_type=user_type).first()
            if user is None:
                raise forms.ValidationError('입력하신 회원 유형이 일치하지 않습니다.')
            
            # 실제 인증 시도
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError(
                    "아이디 또는 비밀번호가 올바르지 않습니다."
                )
            
        return self.cleaned_data

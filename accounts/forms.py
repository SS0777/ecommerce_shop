from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    marketing_agree = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 
                 'phone_number', 'address', 'marketing_agree')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile_image', 'bio', 
                 'phone_number', 'address')
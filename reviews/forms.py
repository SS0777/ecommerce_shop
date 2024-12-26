from django import forms
from .models import Review, Report
from .widgets import MultipleImageInput

class ReviewForm(forms.ModelForm):
    images = forms.ImageField(
        widget=MultipleImageInput(attrs={'class': 'form-control'}),
        required=False,
        label='이미지'
    )

    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'description']
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
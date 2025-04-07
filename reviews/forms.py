# reviews/forms.py
from django import forms
from .models import Review, Report, ReviewImage
from .widgets import MultipleImageInput

class ReviewForm(forms.ModelForm):
    images = forms.FileField(
        required=False,
        widget=MultipleImageInput(),
        label='이미지 업로드',
        help_text='여러 장의 이미지를 선택할 수 있습니다.'
    )

    class Meta:
        model = Review
        fields = ['rating', 'content']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        review = super().save(commit=False)
        if commit:
            review.save()

            # 이미지 저장
            image_files = self.files.getlist('images')
            for image in image_files:
                ReviewImage.objects.create(
                    review=review,
                    image=image
                )

        return review


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['report_type', 'description']
        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
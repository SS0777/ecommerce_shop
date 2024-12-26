from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Report
from .forms import ReviewForm, ReportForm


@login_required
def create_review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product_id = product_id
            review.save()
            
            # 이미지 처리
            for image in request.FILES.getlist('images'):
                ReviewImage.objects.create(
                    review=review,
                    image=image
                )
            
            # 알림 발송
            send_notification(
                review.product.seller,
                'review',
                '새로운 리뷰가 등록되었습니다.',
                f'{review.user.username}님이 상품 리뷰를 작성했습니다.',
                review
            )
            
            return redirect('products:detail', product_id=product_id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create.html', {'form': form})

@login_required
def report_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.review = review
            report.reporter = request.user
            report.save()
            
            # 관리자에게 알림 발송
            admin_users = User.objects.filter(is_staff=True)
            for admin in admin_users:
                send_notification(
                    admin,
                    'system',
                    '새로운 리뷰 신고가 접수되었습니다.',
                    f'리뷰 ID: {review.id}에 대한 신고가 접수되었습니다.',
                    report
                )
            
            return redirect('products:detail', product_id=review.product.id)
    else:
        form = ReportForm()
    
    return render(request, 'reviews/report.html', {'form': form, 'review': review})
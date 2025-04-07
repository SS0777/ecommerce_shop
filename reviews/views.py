from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db import transaction
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Review, Report, ReviewImage
from .forms import ReviewForm, ReportForm
from products.models import Product

User = get_user_model()

@login_required
def create_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # 이미 리뷰를 작성했는지 확인
    if Review.objects.filter(user=request.user, product=product).exists():
        messages.error(request, '이미 이 상품에 대한 리뷰를 작성하셨습니다.')
        return redirect('products:detail', product_id=product_id)
    
    # 상품을 구매한 사용자인지 확인하는 로직 추가 필요
    # if not Order.objects.filter(user=request.user, product=product, status='completed').exists():
    #     messages.error(request, '구매한 상품에 대해서만 리뷰를 작성할 수 있습니다.')
    #     return redirect('products:detail', product_id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    review = form.save(commit=False)
                    review.user = request.user
                    review.product = product
                    review.save()

                    # 이미지 처리
                    images = request.FILES.getlist('images')
                    if images:
                        for image in images:
                            ReviewImage.objects.create(
                                review=review,
                                image=image
                            )

                    # 판매자에게 알림 발송
                    try:
                        send_notification(
                            review.product.seller,
                            'review',
                            '새로운 리뷰가 등록되었습니다.',
                            f'{review.user.username}님이 상품 "{product.name}"에 대한 리뷰를 작성했습니다.',
                            review
                        )
                    except Exception as e:
                        # 알림 발송 실패를 로깅하지만, 리뷰 저장은 계속 진행
                        print(f"Failed to send notification: {e}")

                messages.success(request, '리뷰가 성공적으로 등록되었습니다.')
                return redirect('products:detail', product_id=product_id)

            except Exception as e:
                messages.error(request, '리뷰 등록 중 오류가 발생했습니다. 다시 시도해 주세요.')
                print(f"Error creating review: {e}")
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/create.html', {
        'form': form,
        'product': product
    })

@login_required
def report_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # 자신의 리뷰는 신고할 수 없음
    if review.user == request.user:
        messages.error(request, '자신의 리뷰는 신고할 수 없습니다.')
        return redirect('products:detail', product_id=review.product.id)
    
    # 이미 신고한 리뷰인지 확인
    if Report.objects.filter(review=review, reporter=request.user).exists():
        messages.error(request, '이미 신고한 리뷰입니다.')
        return redirect('products:detail', product_id=review.product.id)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    report = form.save(commit=False)
                    report.review = review
                    report.reporter = request.user
                    report.save()

                    # 관리자에게 알림 발송
                    admin_users = User.objects.filter(is_staff=True)
                    for admin in admin_users:
                        try:
                            send_notification(
                                admin,
                                'system',
                                '새로운 리뷰 신고가 접수되었습니다.',
                                f'리뷰 ID: {review.id} ({review.product.name})에 대한 신고가 접수되었습니다.\n'
                                f'신고 사유: {report.get_report_type_display()}\n'
                                f'신고자: {request.user.username}',
                                report
                            )
                        except Exception as e:
                            print(f"Failed to send notification to admin {admin.username}: {e}")

                messages.success(request, '신고가 접수되었습니다.')
                return redirect('products:detail', product_id=review.product.id)

            except Exception as e:
                messages.error(request, '신고 접수 중 오류가 발생했습니다. 다시 시도해 주세요.')
                print(f"Error creating report: {e}")
    else:
        form = ReportForm()
    
    return render(request, 'reviews/report.html', {
        'form': form,
        'review': review
    })

@login_required
def my_reviews_view(request):
    reviews = Review.objects.filter(user=request.user).select_related(
        'product'
    ).prefetch_related(
        'images'
    ).order_by('-created_at')
    
    return render(request, 'reviews/my_reviews.html', {
        'reviews': reviews
    })

def send_notification(user, notification_type, subject, message, related_object):
    """
    알림을 발송하는 함수
    
    Args:
        user: 알림을 받을 사용자
        notification_type: 알림 유형 (review, system 등)
        subject: 알림 제목
        message: 알림 내용
        related_object: 관련 객체 (Review 또는 Report)
    """
    if not settings.DEBUG:  # 개발 환경에서는 이메일 발송 스킵
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Failed to send email: {e}")
            
    # 여기에 추가적인 알림 로직 구현 가능
    # 예: 푸시 알림, 웹소켓 알림 등
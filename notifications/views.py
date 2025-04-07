from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification, EmailNotification
from django.core.mail import send_mail
from django.template.loader import render_to_string

@login_required
def notification_list(request):
    # 로그인한 사용자의 알림을 가져와서 최신순으로 정렬
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    # 알림을 읽음 처리하는 뷰
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

def send_notification(user, type, title, message, related_object=None):
    # 알림을 생성하고 이메일로 알림을 발송하는 함수
    notification = Notification.objects.create(
        recipient=user,
        notification_type=type,
        title=title,
        message=message,
        content_object=related_object
    )
    
    # 이메일 발송
    if user.profile.marketing_agree:  # 사용자가 마케팅 수신에 동의한 경우
        email_content = render_to_string('notifications/email_template.html', {
            'user': user,
            'notification': notification
        })
        
        # 이메일 알림 객체 생성
        email_notification = EmailNotification.objects.create(
            user=user,
            subject=title,
            content=email_content,
            status='pending',  # 대기 상태로 이메일 생성
        )
        
        # 이메일 발송
        send_mail(
            subject=title,
            message=message,
            from_email='no-reply@shop.com',
            recipient_list=[user.email]
        )
        
        # 이메일 발송 후 상태 업데이트
        email_notification.status = 'sent'  # 이메일 전송 후 상태를 'sent'로 업데이트
        email_notification.sent_at = notification.created_at  # 발송 시각을 알림 생성 시각으로 설정
        email_notification.save()

    return notification

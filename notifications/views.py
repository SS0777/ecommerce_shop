from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.core.mail import send_mail
from django.template.loader import render_to_string

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifications': notifications})

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(
        Notification, 
        id=notification_id, 
        recipient=request.user
    )
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})

def send_notification(user, type, title, message, related_object=None):
    notification = Notification.objects.create(
        recipient=user,
        notification_type=type,
        title=title,
        message=message,
        content_object=related_object
    )
    
    # 이메일 발송
    if user.profile.marketing_agree:
        email_content = render_to_string('notifications/email_template.html', {
            'user': user,
            'notification': notification
        })
        
        EmailNotification.objects.create(
            user=user,
            subject=title,
            content=email_content
        )
        
        send_mail(
            subject=title,
            message=message,
            from_email='no-reply@shop.com',
            recipient_list=[user.email]
        )
    
    return notification
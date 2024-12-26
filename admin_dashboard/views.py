from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate
from .models import DailySales, Settlement
from orders.models import Order
from products.models import Product
from django.utils import timezone

@staff_member_required
def dashboard(request):
    # 기간별 매출 통계
    today = timezone.now().date()
    thirty_days_ago = today - timezone.timedelta(days=30)
    
    daily_sales = Order.objects.filter(
        created_at__date__gte=thirty_days_ago,
        status='paid'
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        total_sales=Sum('total_amount'),
        order_count=Count('id'),
        average_order_value=Avg('total_amount')
    ).order_by('date')

    # 베스트셀러 상품
    best_sellers = OrderItem.objects.values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_sales=Sum('price')
    ).order_by('-total_quantity')[:10]

    # 회원 통계
    user_stats = {
        'total_users': User.objects.count(),
        'new_users_today': User.objects.filter(date_joined__date=today).count(),
        'active_users': User.objects.filter(last_login__date__gte=thirty_days_ago).count()
    }

    context = {
        'daily_sales': daily_sales,
        'best_sellers': best_sellers,
        'user_stats': user_stats
    }
    return render(request, 'admin_dashboard/dashboard.html', context)

@staff_member_required
def sales_report(request):
    start_date = request.GET.get('start_date', thirty_days_ago)
    end_date = request.GET.get('end_date', today)
    
    sales_data = Order.objects.filter(
        created_at__date__range=[start_date, end_date],
        status='paid'
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        total_sales=Sum('total_amount'),
        order_count=Count('id')
    ).order_by('date')
    
    return render(request, 'admin_dashboard/sales_report.html', {'sales_data': sales_data})

@staff_member_required
def settlement_management(request):
    sellers = User.objects.filter(is_staff=False)
    settlements = Settlement.objects.all().order_by('-created_at')
    
    context = {
        'sellers': sellers,
        'settlements': settlements
    }
    return render(request, 'admin_dashboard/settlements.html', context)
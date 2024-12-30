from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Order
import requests

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'orders/cart.html', {'cart': cart})

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        order = Order.objects.create(
            user=request.user,
            shipping_address=request.POST['shipping_address'],
            payment_method=request.POST['payment_method'],
            total_amount=cart.total_price
        )
        
        # 결제 처리 (아임포트 API 연동 예시)
        payment_data = {
            'merchant_uid': f'order_{order.id}',
            'amount': order.total_amount,
            'buyer_email': request.user.email,
            'buyer_name': request.user.username,
        }
        
        response = requests.post(
            'https://api.iamport.kr/payments/prepare',
            data=payment_data
        )
        
        if response.status_code == 200:
            return JsonResponse({'order_id': order.id})
        
        return JsonResponse({'error': '결제 처리 중 오류가 발생했습니다.'})
        
    return render(request, 'orders/checkout.html')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


def history_view(request):
    # 주문내역 뷰 로직
    return render(request, 'orders/history.html')
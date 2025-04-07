from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import SellerRequiredMixin
from .models import Product  # Product 모델 import
from .models import Order

class DashboardView(SellerRequiredMixin, LoginRequiredMixin, TemplateView):  # 순서 수정
    template_name = 'seller/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_sales'] = self.request.user.sales.count()
        context['recent_orders'] = self.request.user.seller_orders.all()[:5]
        return context

class ProductListView(SellerRequiredMixin, LoginRequiredMixin, ListView):  # 순서 수정
    template_name = 'seller/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'seller/product_form.html'
    fields = ['name', 'description', 'price', 'stock', 'image']

    def form_valid(self, form):
        form.instance.seller = self.request.user  # 현재 로그인한 사용자를 판매자로 설정
        return super().form_valid(form)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'seller/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # 현재 로그인한 판매자의 주문 목록만 가져오도록 필터링
        return Order.objects.filter(seller=self.request.user)
    
class StatsView(TemplateView):
    template_name = "seller/stats.html"

class ProfileView(TemplateView):
    template_name = "seller/profile.html" 

class SettingsView(TemplateView):
    template_name = "seller/settings.html"  # 설정 페이지 템플릿
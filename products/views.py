from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from django.views.generic import ListView, DetailView
from .models import Product
from django.utils import timezone
from datetime import timedelta

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if category:
            queryset = queryset.filter(category__slug=category)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search)
            )
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context

@login_required
def toggle_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # 좋아요를 토글 (추가 또는 삭제)
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        is_liked = False
    else:
        product.likes.add(request.user)
        is_liked = True

    # 좋아요 갱신 후 인기 점수 업데이트
    product.update_popularity()

    return JsonResponse({'is_liked': is_liked})

def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'products/search_results.html', {'products': products, 'query': query})

class PopularProductsView(ListView):
    model = Product
    template_name = 'products/popular_products.html'
    context_object_name = 'popular_products'

    def get_queryset(self):
        # 인기 제품을 popularity 기준으로 조회
        queryset = Product.objects.order_by('-popularity')[:10]
        
        # 데이터가 없을 경우, 빈 쿼리셋을 반환하도록 설정
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 제품이 없을 때 "데이터가 없습니다"라는 메시지를 추가
        if not context['popular_products']:
            context['no_data_message'] = "현재 인기 제품이 없습니다."
        return context

class NewProductsView(ListView):
    model = Product
    template_name = 'products/new_products.html'
    context_object_name = 'new_products'

    def get_queryset(self):
        # 7일 이내에 등록된 상품들을 가져옴
        seven_days_ago = timezone.now() - timedelta(days=7)
        return Product.objects.filter(
            created_at__gte=seven_days_ago,
            is_active=True
        ).order_by('-created_at')[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not context['new_products']:
            context['no_data_message'] = "현재 새로운 제품이 없습니다."
        return context
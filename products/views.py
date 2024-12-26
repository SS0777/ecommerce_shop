from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category
from django.views.generic import ListView, DetailView
from .models import Product

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
    if product.likes.filter(id=request.user.id).exists():
        product.likes.remove(request.user)
        is_liked = False
    else:
        product.likes.add(request.user)
        is_liked = True
    return JsonResponse({'is_liked': is_liked})
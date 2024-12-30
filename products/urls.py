from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('like/<int:product_id>/', views.toggle_like, name='toggle_like'),
    path('search/', views.search, name='search'),
    path('popular/', views.PopularProductsView.as_view(), name='popular'),  # 'popular/' 경로 수정
    path('new/', views.NewProductsView.as_view(), name='new'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
]
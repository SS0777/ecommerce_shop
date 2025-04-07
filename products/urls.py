from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # 찜 목록 관련 URL
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),  # 찜 목록 보기
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),  # 찜 목록에 상품 추가
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),  # 찜 목록에서 상품 제거
    path('', views.ProductListView.as_view(), name='product_list'),
    path('like/<int:product_id>/', views.toggle_like, name='toggle_like'),
    path('search/', views.search, name='search'),
    path('popular/', views.PopularProductsView.as_view(), name='popular'),
    path('new/', views.NewProductsView.as_view(), name='new'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]

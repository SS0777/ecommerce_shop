# buyer/urls.py
from django.urls import path
from . import views

app_name = 'buyer'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('orders/', views.OrderHistoryView.as_view(), name='orders'),
]
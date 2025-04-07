# seller/urls.py
from django.urls import path
from . import views

app_name = 'seller'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/add/', views.ProductCreateView.as_view(), name='product-add'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('stats/', views.StatsView.as_view(), name='stats'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
]
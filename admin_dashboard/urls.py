from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('sales/', views.sales_report, name='sales_report'),
    path('settlements/', views.settlement_management, name='settlements'),
]
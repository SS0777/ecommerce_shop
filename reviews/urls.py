from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('create/<int:product_id>/', views.create_review, name='create'),
    path('report/<int:review_id>/', views.report_review, name='report'),
]
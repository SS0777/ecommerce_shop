from django.shortcuts import render

# buyer/views.py
from .mixins import BuyerRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView


class HomeView(TemplateView):
    template_name = 'buyer/home.html'

class CartView(BuyerRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'buyer/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_items'] = self.request.user.cart.all()
        return context
    
class BuyerView(BuyerRequiredMixin, TemplateView):
    template_name = "buyer/home.html"

class ProfileView(TemplateView):
    template_name = "buyer/profile.html"

class WishlistView(TemplateView):
    template_name = "buyer/wishlist.html"

class OrderHistoryView(TemplateView):
    template_name = "buyer/order_history.html"
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

class SellerRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_seller:
            raise PermissionDenied("판매자만 접근할 수 있습니다.")
        return super().dispatch(request, *args, **kwargs)
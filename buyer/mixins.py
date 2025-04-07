# buyer/mixins.py

from django.contrib.auth.mixins import LoginRequiredMixin

class BuyerRequiredMixin(LoginRequiredMixin):
    # 여기에서 필요한 추가적인 로직을 넣을 수 있습니다
    pass

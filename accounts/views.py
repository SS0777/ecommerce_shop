from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from .forms import SignUpForm, ProfileUpdateForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from .models import User


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)
        return response


class LoginView(DjangoLoginView):  # 로그인 뷰 추가
    template_name = 'accounts/login.html'  # 로그인에 사용할 템플릿
    # 기본적으로 'registration/login.html' 템플릿을 사용하지만, 'accounts/login.html'을 사용하려면
    # 이렇게 명시적으로 템플릿을 지정해야 합니다.

class LogoutView(DjangoLogoutView):  # 로그아웃 뷰 추가
    next_page = reverse_lazy('login')  # 로그아웃 후 리디렉션할 URL, 로그인 페이지로 리디렉션

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'orders': request.user.order_set.all()[:5],
        'reviews': request.user.review_set.all()[:5]
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def follow_toggle(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if request.user.following.filter(id=user_id).exists():
        request.user.following.remove(user_to_follow)
        is_following = False
    else:
        request.user.following.add(user_to_follow)
        is_following = True
    
    return JsonResponse({'is_following': is_following})

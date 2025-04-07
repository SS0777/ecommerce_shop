from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import UpdateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.views import LoginView as DjangoLoginView, LogoutView as DjangoLogoutView
from .forms import SignUpForm, ProfileUpdateForm, LoginForm, UserUpdateForm  # UserUpdateForm 임포트 추가
from .models import User


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        # 폼 데이터 저장
        response = super().form_valid(form)
        user = self.object  # 생성된 사용자 객체
        
        # 판매자인 경우 추가 정보 저장
        if form.cleaned_data['user_type'] == 'SELLER':
            user.profile.business_number = form.cleaned_data['business_number']
            user.profile.store_name = form.cleaned_data['store_name']
            user.profile.store_description = form.cleaned_data['store_description']
            user.profile.save()
        
        # 로그인 처리
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        if user:
            login(self.request, user)
            
        return response

    def form_invalid(self, form):
        # 폼 에러 확인을 위한 디버깅 출력
        print(form.errors)
        return super().form_invalid(form)


class LoginView(DjangoLoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('main:home')  # 로그인 성공 후 리다이렉트할 URL

    def get_form_kwargs(self):
        # get_form_kwargs 메소드에서 request를 폼에 전달
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # request를 폼에 전달
        return kwargs

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        user_type = form.cleaned_data.get('user_type')
        user = User.objects.filter(username=username, user_type=user_type).first()

        if user is None:
            form.add_error(None, '입력하신 회원 유형이 일치하지 않습니다.')
            return self.form_invalid(form)

        return super().form_valid(form)

class LogoutView(DjangoLogoutView):  # 로그아웃 뷰 추가
    next_page = reverse_lazy('accounts:login')  # 로그아웃 후 리디렉션할 URL, 로그인 페이지로 리디렉션

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': request.user.orders.all()[:5],  # 수정된 부분: order_set -> orders
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

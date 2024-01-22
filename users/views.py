import random

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView, TemplateView
from django.contrib.auth.views import LoginView as BaseLoginView

from users.forms import CustomUserCreationForm, UserProfileForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация',
    }


def logout_view(request):
    logout(request)
    return redirect('/')  # на главную страницу сайта


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    
    def get_object(self, queryset=None):
        return self.request.user


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save()
            send_mail(
                subject='Подтверждение почты',
                message=f'Код {new_user.code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()
    return redirect(reverse('catalog:index'))


class VerificationTemplateView(TemplateView):
    template_name = 'users/msg_email.html'
    
    def post(self, request):
        code = request.POST.get('code')
        user_code = User.objects.filter(code=code).first()
        
        if user_code is not None and user_code.code == code:
            user_code.is_active = True
            user_code.save()
            return redirect('users:login')
        else:
            return redirect('users:verify_email_error')

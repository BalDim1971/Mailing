import random

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, CreateView, TemplateView, ListView
from django.contrib.auth.views import LoginView as BaseLoginView

from users.forms import CustomUserCreationForm, UserProfileForm, ModeratorForm
from users.models import User
from users.services import send_mail_user, send_sms


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    extra_context = {
        'title': 'Авторизация',
    }


def logout_view(request):
    logout(request)
    return redirect('/')  # на главную страницу сайта


class UserProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:login')
    
    def test_func(self):
        _user = self.request.user
        if self.request.user == self.get_object() or _user.has_perms(['users.set_is_active', ]):
            return True
        return self.handle_no_permission()

    def get_form_class(self):
        if self.request.user == self.get_object():
            return UserProfileForm
        elif self.request.user.has_perm('users.set_is_active'):
            return ModeratorForm


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify_email')
    
    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.save()
        verify_code = User.objects.make_random_password(length=15)
        verify_phone = User.objects.make_random_password(length=15)
        new_user.email_verified = verify_code
        new_user.phone_verified = verify_phone
        new_user.save()
        result_send = send_mail_user(
            subject='Подтверждение регистрации',
            message=f' Для получения полного доступа, введите код активации: {verify_code}',
            email_list=[new_user.email]
        )

        result_sms = send_sms(phone=new_user.phone, message=verify_phone)

        print(result_send, result_sms, sep='\n\n')
        print(f'{new_user} Введите код активации: {verify_code}')
        print(f'{new_user.phone} код верификации: {verify_phone}')
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
    return redirect(reverse('mailing_service:home'))


class VerificationTemplateView(TemplateView):
    template_name = 'users/msg_email.html'
    
    @staticmethod
    def post(request):
        verify_pass = request.POST.get('verify_pass')
        user_code = User.objects.filter(email_verified=verify_pass).first()
        user_phone = User.objects.filter(phone_verified=verify_pass).first()
        if user_code:
            user_code.is_email = True
            user_code.is_active = True
            user_code.save()
            result_send = send_mail_user(
                subject='Успешная активация',
                message='Код активации принят',
                email_list=[user_code.email]
            )
            print(result_send)
            return redirect('users:login')
        if user_phone:
            user_phone.is_phone = True
            user_phone.is_active = True
            user_phone.save()
            result_sms = send_sms(phone=user_phone.phone, message='Добро пожаловать')
            print(f'Верификация телефона {user_phone.phone} прошла успешно')
            print(result_sms)
            return redirect('users:login')
        else:
            return redirect('users:verify_email')
        

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    extra_context = {'title': 'Пользователи', }
    template_name = 'users/users_list.html'

    def test_func(self):
        _user = self.request.user
        if _user.has_perms(['users.set_is_active', ]):
            return True
        return self.handle_no_permission()

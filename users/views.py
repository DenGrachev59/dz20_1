import random
import uuid

from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site

from django.contrib import messages

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

from django.views.generic import CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView

from catalog.models import Product
from services.mixins import UserIsNotAuthenticated
from users.forms import UserRegisterForm, UserPofileForm, UserRecoveryPasswordForm

from users.models import User


class GetContextDataMixin:

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        all_product = Product.objects.all()
        context['all_product_list'] = all_product
        return context


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass


class RegisterView(UserIsNotAuthenticated, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.is_active = False
            self.object.register_uuid = uuid.uuid4().hex
            self.object.save()
            current_site = get_current_site(self.request)
            send_mail(
                subject='Верификация пользователя',
                message=f'Верификация пользователя пройдите по ссылке http://127.0.0.1:8000{reverse_lazy("users:success_register", kwargs={"register_uuid": self.object.register_uuid})}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.object.email]
            )
            return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy('users:login')


def verification_user(request, *args, **kwargs):
    user = User.objects.get(register_uuid=kwargs['register_uuid'])
    if user.register_uuid == kwargs['register_uuid']:
        user.is_active = True
        user.save()

    return redirect(reverse('users:login'))


class ProfileView(GetContextDataMixin, UpdateView):
    model = User
    form_class = UserPofileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):  # Редактирование текущего пользователя который вошел на сайт
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль :{new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]

    )
    request.user.set_password(new_password)
    request.user.save()

    return redirect(reverse('users:login'))



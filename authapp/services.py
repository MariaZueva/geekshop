from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from authapp.forms import ShopUserLoginForms, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser


def send_verify_email(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    full_verify_link = f'{settings.BASE_URL}{verify_link}'

    message = f'You activation url {full_verify_link}'

    return send_mail(
        'Accaunt activate',
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False)
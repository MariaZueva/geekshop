from django.contrib import auth
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

from authapp.forms import ShopUserLoginForms, ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from authapp.services import send_verify_email


def login(request):
    title = 'вход'
    login_form = ShopUserLoginForms(data=request.POST)

    next_p = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('index'))

    content = {'title': title, 'login_form': login_form, 'next': next_p}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save()
            send_verify_email(new_user)
            return HttpResponseRedirect(reverse('index'))
    else:
        register_form = ShopUserRegisterForm()
    content = {'register_form': register_form}
    return render(request, 'authapp/register.html', content)


def edit(request):
    if request.method == 'POST':
        user_edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if user_edit_form.is_valid():
            user_edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        user_edit_form = ShopUserEditForm(instance=request.user)

    content = {'user_edit_form': user_edit_form}
    return render(request, 'authapp/edit.html', content)


def verify(request, email, key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == key and not user.is_activation_key_expired():
            user.save_user()
    return render(request, 'authapp/register_result.html')






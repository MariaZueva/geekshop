import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.conf import settings


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True, verbose_name='аватар')
    age = models.PositiveSmallIntegerField(verbose_name='возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) > self.activation_key_expires + timedelta(hours=48):
            return True
        return False

    def activate_user(self):
        self.is_active = True
        self.activation_key = None
        self.activation_key_expires = None
        self.save()


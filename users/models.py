import random

from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager, send_mail
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice(
                    'abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))
                
        extra_fields['phone_number'] = phone_number
        return super()._create_user(username, email, password, **extra_fields)

    def create_superuser(
        self,
        username=None,
        phone_number=None,
        email=None,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            username=username,
            phone_number=phone_number,
            email=email,
            password=password,
            **extra_fields
        )

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractUser):
    phone_number = models.BigIntegerField(_('mobile number'), unique=True, null=True, blank=True,
                                          validators=[
                                              validators.RegexValidator(
                                                  r'^989[0-3,9]\d{8}$', ('Enter a valid mobile number.'))
    ],
        error_messages={
                                              'unique': _("A user whit this mobile number already exists.")
    })

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_('nick_name'), max_length=150, blank=True)
    avatar = models.ImageField(_('avatar'), blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    gender = models.BooleanField(_('gender'), help_text=_(
        'female is False, male is True, Null is unset'), null=True, blank=True)
    province = models.ForeignKey(verbose_name=_(
        'province'), to='Province', null=True, on_delete=models.SET_NULL)
    # email = models.EmailField(_('email address', blank=True))
    # phone_number = models.BigIntegerField(_('mobile number'), blank=True, null=True,
    #                                       validators=[
    #                                           validators.RegexValidator(
    #                                               r'^989[0-3,9]\d{8}$', ('Enter a valid mobile number.'))])

    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('profile')


class Device(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android')
    )

    user = models.ForeignKey(
        User, related_name='devices', on_delete=models.CASCADE)
    device_uuid = models.UUIDField(_('Device UUid'), null=True)
    last_login = models.DateField(_('last login date'), null=True)
    device_type = models.PositiveSmallIntegerField(
        choices=DEVICE_TYPE_CHOICES, default=WEB)
    device_os = models.CharField(_('device model'), max_length=50, blank=True)
    device_model = models.CharField(
        _('app version'), max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_devices'
        verbose_name = _('device')
        verbose_name_plural = _('devices')
        unique_together = ('user', 'device_uuid')


class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

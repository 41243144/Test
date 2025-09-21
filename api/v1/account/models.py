from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('必須提供 email')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email       = models.EmailField('電子郵件', unique=True)
    is_active   = models.BooleanField('是否啟用', default=True)
    is_staff    = models.BooleanField('是否員工', default=False)
    date_joined = models.DateTimeField('加入時間', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    user        = models.OneToOneField(
                      settings.AUTH_USER_MODEL,
                      on_delete=models.CASCADE,
                      related_name='profile'
                  )
    real_name   = models.CharField('真實姓名', max_length=20, blank=True, null=True)
    nickname    = models.CharField('暱稱', max_length=20, blank=True, null=True)
    portrait    = models.ImageField(
                      '頭像',
                      upload_to='user/portrait/',
                      blank=True, null=True
                  )
    address     = models.CharField('通訊地址', max_length=255, blank=True, null=True)
    phone       = PhoneNumberField('手機號碼', blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}_Profile"

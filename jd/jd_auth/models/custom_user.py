from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from jd_auth.managers import UserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin



class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        _("username"),
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    email = models.EmailField(
        _("email address"), 
        null=True,
        blank=True,
        unique=True
    )
    phone = models.CharField(
        _("phone number"),
        max_length=20,
        null=True,
        blank=True,
        unique=True
    )
    date_joined = models.DateTimeField(
        _("date joined"),
        auto_now_add=True,
    )
    is_active = models.BooleanField(
        _("active"),
        default=False
    )
    is_staff = models.BooleanField(
        _("staff"),
        default=False
    )
    is_verified = models.BooleanField(
        _("verified"),
        default=False
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        unique_together = ("username", "email", "phone") #составной ключ пользователя

    def __str__(self):
        return str(self.pk)
    

    
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from .profile_basket import Basket
from .profile_user import Profile

@receiver(post_save, sender=User)
def create_profile_models(sender, created, instance, **kwargs):

    """
    сигнал, при созданий пользователя создается профиль и корзина
    """

    if created:
        Profile.objects.create(user=instance)
        Basket.objects.create(user=instance)


    
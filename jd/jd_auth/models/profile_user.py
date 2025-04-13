from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        "User",
        on_delete=models.CASCADE
    )
    first_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        default=None,
        verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=75,
        null=True,
        blank=True,
        default=None,
        verbose_name="Фамилия"
    )
    link_tg = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        default=None,
        verbose_name="телеграмм ссылка"
    )
    
    





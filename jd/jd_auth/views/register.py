from django.views.generic import FormView
from jd_auth.forms import CustomUserCreateForm
from django.urls import reverse_lazy
from jd_auth.models import User
from django.shortcuts import redirect
from uuid import uuid4
from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from jd_auth.utils import send_code_confirm_phone
from os import getenv




API_URL=getenv("API_AUTHENTICATE_URL")


"""
шаблон регистраций
"""

def register_for_email(self, user, form):

    """
    тут происходит отправка писем для подтверждения почты
    """

    # сохраняем пароль пользователя
    user.set_password(form.cleaned_data.get("password"))
    user.save()

    token = uuid4().hex
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    cache.set(
        redis_key, 
        {"user_id" : user.id}, 
        timeout=settings.SOAQAZ_USER_CONFIRMATION_TIMEOUT
    )

    confirm_link = self.request.build_absolute_uri(
        reverse_lazy(
            "email_confirm", kwargs={"token": token}
        )
    )

    message = _(f'follow this link %s \n' f"to confirm! \n" % confirm_link)

    send_mail(
        subject=_("Please confirm your registration!"),
        message=message,
        from_email="Eltrox822@yandex.ru",
        recipient_list=[user.email, ]
    )

    

class RegisterView(FormView):
    form_class = CustomUserCreateForm
    template_name = "jd_auth/register.html"
    success_url = reverse_lazy("login")


    def form_valid(self, form):

        user = User.objects.get(
            phone=form.cleaned_data.get("phone"),
            email=form.cleaned_data.get("email")
        )

        if user.email:
            register_for_email(self, user, form)

        elif user.phone:
            if send_code_confirm_phone(self, user):
                return redirect("phone_confirm")
            else:
                return redirect("register")

        return super().form_valid(form)




    

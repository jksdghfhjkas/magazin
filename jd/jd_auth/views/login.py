from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login as auth_login 
from jd_auth.utils import send_code_confirm_phone
from django.views.generic import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from jd_auth.forms import LoginForm
from django.contrib import messages
from jd_auth.models import User
from os import getenv

"""
авторизация по телефону или почте

через телефон:
получаем пользователя и вызываем send_code_confirm_phone
которая отправляет код боту и возращает true если все отправилось
переходим на подтвержение номера

через почту:
просто получаем почту и пароль 
и авторизовываем
"""

API_URL = getenv("API_AUTHENTICATE_URL")


class LoginView(FormView):
    form_class = LoginForm
    template_name = "jd_auth/login.html"

    def form_valid(self, form):

        if phone := form.cleaned_data.get("phone"):

            try:
                user = User.objects.get(phone=phone)
                if send_code_confirm_phone(self, user):
                    return redirect("phone_confirm")
                else:
                    return redirect("login")
                
            except User.DoesNotExist:
                messages.error(self.request, "Пользователь не найден.")
                return redirect("login")
            

        elif email := form.cleaned_data.get("email"):
            try:
                user = User.objects.get(email=email)
                password = form.cleaned_data.get("password")

                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    self.request.session["Authorization"] = str(refresh.access_token)
                    auth_login(self.request, user)
                    return redirect("profile")
                else:
                    messages.error(self.request, "Неверный пароль!")
                    return redirect("login")

            except User.DoesNotExist:
                messages.error(self.request, "Пользователь не найден.")
                return redirect("login")


        messages.error(self.request, "Что то пошло не так!")
        return redirect("login")
    

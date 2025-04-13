from django.shortcuts import render, get_object_or_404, redirect
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login as auth_login 
from jd_auth.utils import encode_jwt
from jd_auth.models import User
from os import getenv
import requests


API_URL=getenv("API_AUTHENTICATE_URL")

"""
представление для подтверждения номера телефона и авторизаций

получаем код и номером телефона из сессий (они там появляются после вызова send_code_confirm_phone)
дальше подтверждаем номер если нужно и авторизовываем
дальше заполняем chat_id
"""

def save_chat_id(user):

    """
    тут отправляем запрос чтобы получить chat_id 
    """
    
    if not user.profile.link_tg:
        url = f"{API_URL}api/v1/get_chat_id/"
        token = encode_jwt({
            "phone": user.phone
        })
        headers = {"token": token}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            user.profile.link_tg = response.json()
            user.profile.save()


def phone_confirm(request):
    message = "Введите код подтверждения"

    if request.method == "POST":
        code = request.POST.get("code")

        if not code or len(code) != 6:
            message = "Код должен состоять из 6 цифр"

        else:
            session_code = request.session.get("verification_code")
            phone = request.session.get("phone")

            if not session_code or not phone:
                message = "Срок действия кода истёк, попробуйте снова"
                return redirect("register")

            elif session_code == code:
                user = get_object_or_404(User, phone=phone)

                if not user.is_verified:

                    # проводим верефикацию пользователя 
                    user.is_verified = True
                    user.is_active = True
                    user.save(update_fields=["is_verified", "is_active"])

                # авторизовываем
                # создаю или получаю рефреш токен и передаю в сессию акцесс токен
                refresh = RefreshToken.for_user(user)
                request.session["Authorization"] = str(refresh.access_token)

                auth_login(request, user)
                save_chat_id(user)

                return redirect("profile")
            
            else:
                message = "Неверный код подтверждения"

    return render(request, "jd_auth/phone_confirm.html", {"message": message})
    
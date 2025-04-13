import jwt
import random
from string import digits
from os import getenv
import datetime
from datetime import timezone
import requests
from django.contrib import messages

API_URL = getenv("API_AUTHENTICATE_URL")
JWT_SECRET_KEY=getenv("JWT_SECRET_KEY")
ALGORITHM=getenv("JWT_ALOGORITHM")


def create_code():
    """
    функция для создания 6 значного кода 
    """
    return "".join(random.choice(digits) for _ in range(6))



def encode_jwt(data):
    """
    функция для создания jwt кода
    """

    payload = {
        "data": data,
        'exp': datetime.datetime.now(timezone.utc) + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)


def send_code_confirm_phone(self, user) -> bool:

    """
    здесь мы отправляем код подтверждения номера на api 
    возращаем true если отправилось иначе false
    """
    try:
        code = create_code()
        data = {
            "phone": user.phone,
            "code": code,
            "chat_id": str(user.profile.link_tg)
        }
        jwt_code = encode_jwt(data)

        url = f"{API_URL}api/v1/confirm_phone"
        headers = {"token": jwt_code}

        response = requests.post(url, headers=headers)
        response.raise_for_status()

        # передаем данные в сессию
        self.request.session['verification_code'] = code
        self.request.session['phone'] = user.phone

        return True
    
    except Exception as error:
        messages.error(self.request, "Не удалось отправить код подтверждения. Попробуйте позже.")
        return False


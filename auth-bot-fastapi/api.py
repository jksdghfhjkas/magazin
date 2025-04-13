from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from aiogram import Dispatcher, Bot
from fastapi import FastAPI, Header, HTTPException
from typing import Annotated

from config import SECRET_KEY, ALGORITHM
from bot import bot, dp
from os import getenv
import asyncio

import redis
import jwt


app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379, db=3)



def decode_jwt(token: str):
    """
    Функция расшифровки JWT токена.
    """
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to decode token: {str(e)}")
    
    
async def start_bot():
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.start_polling()


@app.on_event("startup")
async def on_startup():
    #запускаем бота
    asyncio.create_task(start_bot())


@app.post("/api/v1/confirm_phone/")
async def confirm_phone(token: Annotated[str, Header()]):

    """
    Тут приходит запрос с сайта который присылает jwt токен
    
    структура jwt token

    data : {
        "phone": 182348324,
        "code": 112312,
        "chat_id": str
    },
    Authenticate : SECRET_KEY,
    exp: time
    """

    global redis_client
    decode_data = decode_jwt(token)

    user_data = decode_data.get("data")

    if chat_id := user_data.get("chat_id"):
        try:
            await bot.send_message(chat_id=chat_id, text=f"Ваш код: {user_data.get('code')}\n Хорошего дня!")
        except (ChatNotFound, BotBlocked):
            #если нет доступа к пользователю
            redis_client.set(user_data.get("phone"), user_data.get("code"), ex=60)
    else:
        redis_client.set(user_data.get("phone"), user_data.get("code"), ex=60)

        

@app.get("/api/v1/get_chat_id/")
async def get_chat_id(token: Annotated[str, Header()]):
    """
    получение номера chat_id для авторизаций
    """
    global redis_client
    decode_data = decode_jwt(token)

    data = decode_data.get("data")

    if phone := data.get("phone"):
        chat_id = redis_client.get(phone)
        return chat_id

    else:
        raise HTTPException(status_code=400, detail="Неверные данные")
    


@app.on_event("shutdown")
async def on_shutdown():
    "прекращаем сессию с ботом"
    await bot.session.close()
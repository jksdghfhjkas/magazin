from fastapi import FastAPI, Header, HTTPException
from bot import chat_id_handle_contact
from typing import Annotated
from os import getenv
import uvicorn
import redis
import jwt
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters
from bot import start_messages, handle_contact


SECRET_KEY  = getenv("JWT_SECRET_KEY")
ALGORITHM = getenv("JWT_ALOGORITHM")

app = FastAPI()
redis_client = redis.Redis(host='redis', port=6379, db=3)


# bot
token = getenv("BOT_TOKEN")
application = Application.builder().token(token).build()

application.add_handler(CommandHandler("start", start_messages))
application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
application.run_polling()


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

    global redis_client, application
    decode_data = decode_jwt(token)

    # добавляем данные с сервера в redis
    user_data = decode_data.get("data")

    if chat_id := user_data.get("chat_id"):
        await chat_id_handle_contact(chat_id, user_data.get("code"), application)
    else:
        redis_client.set(user_data.get("phone"), user_data.get("code"), ex=60)


@app.get("api/v1/get_chat_id/")
async def get_chat_id(token: Annotated[str, Header()]):
    global redis_client
    decode_data = decode_jwt(token)

    if phone := decode_data.get("data").get("phone"):
        chat_id = redis_client.get(phone)
        return chat_id

    else:
        raise HTTPException(status_code=400, detail="Неверные данные")



uvicorn.run(app, host="0.0.0.0", port=8001)
    

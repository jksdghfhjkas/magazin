from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, filters
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup

import redis
from os import getenv


redis_client = redis.Redis(host='redis', port=6379, db=3, decode_responses=True)
APPLICATION = None


async def start_messages(update: Update, content: ContextTypes):
    """
    /start 
    просим пользователя отправить номер телефона
    """

    await update.message.reply_text('Привет! Я бот для регистраций')
    
    contact_button = KeyboardButton(text="📱 Отправить номер телефона", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Пожалуйста, отправьте ваш номер телефона, чтобы продолжить:",
        reply_markup=keyboard
    )



async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global redis_client

    """
    функция для обработки номера телефона
    """
    if update.message.contact:
        phone_number = update.message.contact.phone_number  
        chat_id = update.effective_chat.id 

            
        if code := authenticate_user(phone_number):

            await update.message.reply_text(
                f"Спасибо! Код для регистраций: {code}\n Пожалуйста не удаляйте чат он будет использоваться для авторизаций!"
            )

            # заносим chat_id в redis для отправки на сервер
            redis_client.set(phone_number, chat_id, ex=300)

        else:
            await update.message.reply_text(
                f"Вы не регистрировались или время регистраций истекло, повторите попытку! {phone_number}"
            )



async def chat_id_handle_contact(chat_id: str, code: str, application):
    """
    отправка сообщения по chat_id
    """
    
    message = f"Ваш код: {code}\n Хорошего дня!"

    await application.bot.send_message(chat_id=chat_id, text=message)
    



def authenticate_user(phone: str):
    
    """
    структура данных в redis

    phone:code / время 60 секунд
    """
    global redis_client
    code = redis_client.get(phone)

    if not code:
        return False
    
    return code

    
if __name__ == "__main__":
    token = getenv("BOT_TOKEN")
    APPLICATION = Application.builder().token(token).build()

    APPLICATION.add_handler(CommandHandler("start", start_messages))
    APPLICATION.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    APPLICATION.run_polling()

    print("start success...")






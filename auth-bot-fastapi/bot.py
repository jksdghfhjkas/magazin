from aiogram import Dispatcher, Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import TELEGRAM_TOKEN
import redis


bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
redis_client = redis.Redis(host='redis', port=6379, db=3, decode_responses=True)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer('Привет! Я бот для регистраций')
    
    await message.answer(
        "Пожалуйста, отправьте ваш номер телефона, чтобы продолжить:",
        reply_markup=get_contact_keyboard()
        )


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message: types.Message):
    """
    тут мы обрабатываем нажатие кнопки для получение контакта
    """

    contact = message.contact
    phone_number = contact.phone_number

    if contact.user_id == message.from_user.id:
        if code := authenticate_user(phone_number):
            await message.answer(
                f"Спасибо! Код для регистраций: {code}\nПожалуйста не удаляйте чат он будет использоваться для авторизаций!"
            )

            # заносим chat_id в redis для отправки на сервер
            redis_client.set(phone_number, contact.user_id, ex=300)
        else:
            await message.answer(
                f"Вы не регистрировались или время регистраций истекло, повторите попытку!"
            )

    else:
        await message.answer(
            "Это не ваш номер телефона. Пожалуйста, отправьте свой номер.",
            reply_markup=get_contact_keyboard()  # Показываем кнопку еще раз
        )


# utils function

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


def get_contact_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = KeyboardButton("Отправить номер телефона", request_contact=True)
    keyboard.add(contact_button)
    return keyboard
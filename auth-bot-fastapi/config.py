from os import getenv

SECRET_KEY  = getenv("JWT_SECRET_KEY")
ALGORITHM = getenv("JWT_ALOGORITHM")
TELEGRAM_TOKEN = getenv("BOT_TOKEN")


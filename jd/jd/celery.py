import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jd.settings")

app = Celery("parsing", include=[
    "parser.utils.parser_category",
    "parser.utils.parser_product"
])

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


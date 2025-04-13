from django.conf import settings
from django.core.cache import cache
from jd_auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

"""
представление подтверждения почты
"""

def email_confirm(request, token):
    redis_key = redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    user_data = cache.get(redis_key) or {}

    if user_id := user_data.get("user_id"):
        user = get_object_or_404(User, id=user_id)
        user.is_verified = True
        user.is_active = True
        user.save(update_fields=["is_verified", "is_active"])
        return redirect(to=reverse_lazy("login"))
    
    else:
        return redirect(to=reverse_lazy("register"))
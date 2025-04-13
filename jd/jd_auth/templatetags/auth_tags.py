from django import template
from rest_framework_simplejwt.tokens import RefreshToken

register = template.Library()

@register.simple_tag
def get_access_token(request):
    """
    получает токен из сессий 
    """
    if request.user.is_authenticated:
        return request.session.get("Authorization")
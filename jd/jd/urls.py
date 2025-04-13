from django.contrib import admin
from django.urls import path, include
from main.views import ScreensaverView



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", ScreensaverView, name="start"),

    path("catalog/", include("main.urls")),
    path("auth/", include("jd_auth.urls")),

    path("api/v1/", include("test_api.urls"),)
]

from django.urls import path
from jd_auth.views import RegisterView, ProfileView, email_confirm, phone_confirm, LoginView
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(template_name="jd_auth/logout.html"), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email_confirm/<token>/", email_confirm, name="email_confirm"),
    path("phone_confirm/", phone_confirm, name="phone_confirm")

]



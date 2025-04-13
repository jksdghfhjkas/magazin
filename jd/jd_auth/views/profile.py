from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from jd_auth.models import User


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name="jd_auth/profile.html"
    context_object_name="data"

    def get_object(self):
        return self.request.user
    

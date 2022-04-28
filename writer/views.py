from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from authentication.models import UserInformation


class DashboardView(LoginRequiredMixin, View):
    template_name = "writer/dashboard.html"

    def get(self, request, *args, **kwargs):
        user = UserInformation.objects.get(user_id=request.user.id)
        return render(request, self.template_name, {
            'user': user
        })

    def post(self, request, *args, **kwargs):
        pass




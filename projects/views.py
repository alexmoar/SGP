from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class ProjectView(LoginRequiredMixin, View):
    template_name = "administrator/add_project.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        pass



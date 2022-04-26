from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from authentication.models import User


def redirect_session(request):
    if request.user.is_authenticated:
        user_information = User.objects.get(id=request.user.id)
        if user_information:
            # if user_information.role == User.ADMIN:
            return redirect(reverse_lazy('administrator:dashboard'))

    return redirect(reverse_lazy('core:sign_in'))


class SignInView(View):
    template_name = "authentication/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('authentication:redirect_session'))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if User.objects.filter(username__exact=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('authentication:redirect_session'))

        messages.error(request, 'Incorrecto usuario o contraseña. Por favor intentalo de nuevo')
        return redirect(reverse_lazy('authentication:sign_in'))

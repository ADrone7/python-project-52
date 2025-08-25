from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "index.html"


class AuthRequired(LoginRequiredMixin):

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! \
                       Пожалуйста, выполните вход.')
        return redirect('login')

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from .forms import UserCreateForm, UserLoginForm, UserUpdateForm

User = get_user_model()


class UserCreateView(
    SuccessMessageMixin,
    CreateView,
    ):
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserPermission(
    UserPassesTestMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    ):
    model = User
    success_url = reverse_lazy('users:index')

    def test_func(self):
        return self.request.user == self.get_object()

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            message = 'Вы не авторизованы! Пожалуйста, выполните вход.'
            redirect_url = 'login'
        else:
            message = 'У вас нет прав для изменения другого пользователя.'
            redirect_url = 'users:index'
        messages.error(self.request, message)
        return redirect(redirect_url)


class UserUpdateView(
    UserPermission,
    UpdateView,
    ):
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_message = 'Пользователь успешно изменен'


class UserDeleteView(
    UserPermission,
    DeleteView,
    ):
    template_name = 'users/delete.html'
    success_message = 'Пользователь успешно удалён'


class UserListView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_message = 'Вы залогинены'
    
    def get_success_url(self):
        return reverse_lazy('index')
    

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
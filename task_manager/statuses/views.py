from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
)

from task_manager.views import AuthRequired

from .forms import StatusForm
from .models import Status


class StatusCreateView(
    AuthRequired,
    SuccessMessageMixin,
    CreateView,
    ):
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:index')
    success_message = 'Статус успешно добавлен'


class StatusUpdateView(
    AuthRequired,
    SuccessMessageMixin,
    UpdateView,
    ):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_message = 'Статус успешно изменен'
    success_url = reverse_lazy('statuses:index')


class StatusDeleteView(
    AuthRequired,
    SuccessMessageMixin,
    DeleteView,
    ):
    model = Status
    template_name = 'statuses/delete.html'
    success_message = 'Статус успешно удалён'
    success_url = reverse_lazy('statuses:index')


class StatusListView(
    AuthRequired,
    ListView,
    ):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

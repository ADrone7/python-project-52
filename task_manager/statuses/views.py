from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
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
    success_message = 'Статус успешно создан'


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
    success_message = 'Статус успешно удален'
    success_url = reverse_lazy('statuses:index')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if self.object.tasks.exists():
            messages.error(
                request,
                "Невозможно удалить статус, потому что он используется"
            )
            return redirect(self.success_url)
            
        response = super().post(request, *args, **kwargs)
        return response


class StatusListView(
    AuthRequired,
    ListView,
    ):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

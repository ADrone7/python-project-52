from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from task_manager.views import AuthRequired

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(AuthRequired, ListView):
    model = Task
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        queryset = Task.objects.all()
        self.filterset = TaskFilter(self.request.GET, queryset=queryset)

        queryset = self.filterset.qs

        if self.request.GET.get('self_tasks'):
            queryset = queryset.filter(author=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context


class TaskShowView(AuthRequired, DetailView):
    model = Task
    template_name = 'tasks/show.html'
    context_object_name = 'task'


class TaskCreateView(AuthRequired, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks:index')
    success_message = "Задача успешно создана"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequired, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks:index')
    success_message = "Задача успешно изменена"


class TaskDeleteView(AuthRequired, SuccessMessageMixin,
                     UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks:index')
    success_message = "Задача успешно удалена"

    def test_func(self):
        task = self.get_object()
        return task.author == self.request.user

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        messages.error(self.request, "Задачу может удалить только ее автор")
        return redirect(self.success_url)
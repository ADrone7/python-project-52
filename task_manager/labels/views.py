from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.views import AuthRequired

from .forms import LabelForm
from .models import Label


class LabelListView(AuthRequired, ListView):
    model = Label
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelCreateView(AuthRequired, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:index')
    success_message = "Метка успешно создана"


class LabelUpdateView(AuthRequired, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels:index')
    success_message = "Метка успешно изменена"


class LabelDeleteView(AuthRequired, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:index')
    success_message = "Метка успешно удалена"
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if self.object.tasks.exists():
            messages.error(
                request,
                "Невозможно удалить метку, потому что она используется"
            )
            return redirect(self.success_url)
            
        response = super().post(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
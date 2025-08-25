from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']

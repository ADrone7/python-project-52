from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'first_name',
                  'last_name', 'password1', 'password2']
        

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'password']


class UserUpdateForm(UserCreateForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username == self.instance.username:
            return username

        if User.objects.filter(username=username).exclude(
            pk=self.instance.pk).exists():
            raise forms.ValidationError(
                User._meta.get_field('username').error_messages['unique']
            )

        return username
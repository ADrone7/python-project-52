from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Ваш пароль должен содержать как минимум 3 символа."
    )
    password2 = forms.CharField(
        required=True,
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Для подтверждения введите, пожалуйста, пароль ещё раз."
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'имя пользователя',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
            'username': forms.TextInput(attrs={'required': True}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error("password2", "Введенные пароли не совпадают.")

            if len(password1) < 3:
                self.add_error(
                    "password2",
                    "Введённый пароль слишком короткий. Он \
                        должен содержать как минимум 3 символа.",
                )
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
        

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


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
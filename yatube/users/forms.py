from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class EditForm(UserChangeForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'placeholder': 'please enter password'
            }
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control', 'placeholder': 'please enter password'
            }
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f'Пользователь {username} уже существует'
            )
        return username

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email',)

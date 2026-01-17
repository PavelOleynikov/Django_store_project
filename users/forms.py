from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15, required=False, help_text="Необязательное поле. Введите ваш номер телефона"
    )
    username = forms.CharField(max_length=30, required=True, help_text="Обязательное поле.")

    class Meta:
        model = CustomUser
        fields = ("email", "username", "first_name", "last_name", "phone_number", "password1", "password2")

    def __init__(self, *args, **kwargs):
        """Настройка стилей для полей формы"""

        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "form-control", "placeholder": "Введите почту"})
        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Введите имя пользователя"}
        )
        self.fields["first_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите имя"})
        self.fields["last_name"].widget.attrs.update({"class": "form-control", "placeholder": "Введите фамилию"})
        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "89991234567",
                "type": "tel",
                "data-mask": "80000000000",
            }
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Введите пароль"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Повторите пароль"})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Номер телефона должен состоять только из цифр.")
        return phone_number

from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config import settings
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    """Регистрация нового пользователя"""

    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        """Отправляет приветственное письмо пользователю"""

        subject = "Добро пожаловать в наш сервис Skystore!"
        message = "Спасибо, что зарегистрировались в нашем интернет-магазине!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]  # список получателей
        send_mail(subject, message, from_email, recipient_list)

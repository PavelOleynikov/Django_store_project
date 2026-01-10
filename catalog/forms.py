from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product


class ProductForm(forms.ModelForm):
    """Класс-форма для создания и редактирования продуктов с валидацией"""

    # Константа с запрещенными словами
    FORBIDDEN_WORDS = [
        "казино",
        "криптовалюта",
        "крипта",
        "биржа",
        "дешево",
        "бесплатно",
        "обман",
        "полиция",
        "радар",
    ]

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "category",
            "image",
            "price",
        ]

    def _get_forbidden_words_in_text(self, text):
        """Общий метод для поиска запрещенных слов в тексте"""

        if not text:
            return []
        text_lower = text.lower()
        return [word for word in self.FORBIDDEN_WORDS if word in text_lower]

    def clean_name(self):
        """Валидация поля 'name' на запрещенные слова"""

        name = self.cleaned_data.get("name")
        found_words = self._get_forbidden_words_in_text(name)
        if found_words:
            raise ValidationError(f"Название содержит запрещенные слова: " f'{", ".join(found_words)}')
        return name

    def clean_description(self):
        """Валидация поля 'описание' на запрещенные слова"""

        description = self.cleaned_data.get("description")
        found_words = self._get_forbidden_words_in_text(description)
        if found_words:
            raise ValidationError(f"Описание содержит запрещенные слова: " f'{", ".join(found_words)}')
        return description

    def clean_price(self):
        """Валидация поля 'цена' на положительность"""

        price = self.cleaned_data.get("price")
        if price is not None and price <= 0:
            raise ValidationError("Цена должна быть положительной")
        return price

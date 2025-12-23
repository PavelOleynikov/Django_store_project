from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add test products to the database"

    def handle(self, *args, **options):
        Product.objects.all().delete()  # предварительно удаляем все записи из таблиц
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(
            name="Одежда", description="одежда на любой вкус и цвет"
        )

        products = [
            {"name": "свитер", "price": 3500, "category": category},
            {"name": "кофта", "price": 4000, "category": category},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added product: {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Product already exist: {product.name}")
                )

# если необходимо добавить данные из фикстур, то можно использовать такой код:

# from django.core.management import call_command
# from django.core.management.base import BaseCommand
# from catalog.models import Category, Product
#
# class Command(BaseCommand):
#     help = 'Load test data from fixture'
#
#     def handle(self, *args, **kwargs):
#         Product.objects.all().delete()
#         Category.objects.all().delete()
#
#         call_command('loaddata', 'fixtures/category_fixture.json')
#         call_command('loaddata', 'fixtures/product_fixture.json')
#         self.stdout.write(self.style.SUCCESS('Successfully loaded test data from fixtures'))

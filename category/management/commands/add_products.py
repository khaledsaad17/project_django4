from django.core.management.base import BaseCommand
from category.models import Product

class Command(BaseCommand):
    help = 'Adds products to the database'

    def handle(self, *args, **kwargs):
        products = [
            {
                'name': 'Duspatalin Retard | 200 Mg',
                'price': 90,
                'image': 'img/dus.webp',
                'description': 'Duspatalin Retard 200mg capsules',
                'category': 'medication',
                'product_id': 49
            },
            {
                'name': 'Panadol | Extra Tablets for Extra',
                'price': 34,
                'image': 'img/panadol-extra-tab-11664280219.webp',
                'description': 'Panadol Extra tablets',
                'category': 'medication',
                'product_id': 50
            },
            # Add more products here...
        ]

        for product_data in products:
            Product.objects.get_or_create(
                product_id=product_data['product_id'],
                defaults=product_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully added products')) 
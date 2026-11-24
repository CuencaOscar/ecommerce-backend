from django.core.management.base import BaseCommand

from products.models import Product

DEMO_PRODUCTS = [
    ("Wireless Headphones", "Over-ear, active noise cancelling, 30-hour battery.", "129.90", 25),
    ("Mechanical Keyboard", "Hot-swappable switches and per-key RGB backlight.", "89.50", 40),
    ("USB-C Hub", "7-in-1 with 4K HDMI and 100 W power delivery.", "45.00", 60),
    ("Smartwatch", "Heart-rate and GPS tracking, water resistant.", "199.00", 15),
    ("Portable SSD 1 TB", "USB 3.2 Gen 2, up to 1,050 MB/s.", "109.99", 0),
    ("Webcam 1080p", "Autofocus, dual microphones and privacy shutter.", "59.90", 32),
]


class Command(BaseCommand):
    help = "Load a small demo catalog (skips products that already exist)."

    def handle(self, *args, **options):
        created = 0
        for name, description, price, stock in DEMO_PRODUCTS:
            _, was_created = Product.objects.get_or_create(
                name=name, defaults={"description": description, "price": price, "stock": stock}
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"{created} demo products created."))

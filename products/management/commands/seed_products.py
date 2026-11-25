from django.core.management.base import BaseCommand

from products.models import Product

# Product photos from Unsplash (https://unsplash.com/license), served from its CDN.
IMG = "https://images.unsplash.com/{}?w=800&h=600&fit=crop&auto=format&q=80"

DEMO_PRODUCTS = [
    ("Wireless Headphones", "Over-ear, active noise cancelling, 30-hour battery.", "129.90", 25, IMG.format("photo-1546435770-a3e426bf472b")),
    ("Mechanical Keyboard", "Hot-swappable switches and per-key RGB backlight.", "89.50", 40, IMG.format("photo-1589578228447-e1a4e481c6c8")),
    ("USB-C Hub", "7-in-1 with 4K HDMI and 100 W power delivery.", "45.00", 60, IMG.format("photo-1616578273577-5d54546f4dec")),
    ("Smartwatch", "Heart-rate and GPS tracking, water resistant.", "199.00", 15, IMG.format("photo-1579586337278-3befd40fd17a")),
    ("Portable SSD 1 TB", "USB 3.2 Gen 2, up to 1,050 MB/s.", "109.99", 0, IMG.format("photo-1577538926210-fc6cc624fde2")),
    ("Webcam 1080p", "Autofocus, dual microphones and privacy shutter.", "59.90", 32, IMG.format("photo-1623949556303-b0d17d198863")),
    ("Wireless Mouse", "Silent clicks, 4,000 DPI sensor and USB-C charging.", "34.90", 50, IMG.format("photo-1658070429465-848c0796abf3")),
    ("Bluetooth Speaker", "Compact, water resistant, 12 hours of playback.", "49.00", 8, IMG.format("photo-1547052178-7f2c5a20c332")),
]


class Command(BaseCommand):
    help = "Load the demo catalog, creating missing products and refreshing the existing ones."

    def handle(self, *args, **options):
        created = 0
        for name, description, price, stock, image_url in DEMO_PRODUCTS:
            _, was_created = Product.objects.update_or_create(
                name=name,
                defaults={"description": description, "price": price, "stock": stock, "image_url": image_url},
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"{created} demo products created, {len(DEMO_PRODUCTS) - created} updated."))

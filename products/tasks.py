from celery import shared_task
from .models import Brand, Product
from .scraper import scrape_amazon_products
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


@shared_task(bind=True, max_retries=3)
def update_products_for_brand(self, brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
        products = scrape_amazon_products(brand.name)

        for product_data in products:
            product, created = Product.objects.update_or_create(
                asin=product_data['asin'],
                defaults={
                    'name': product_data['name'],
                    'sku': product_data['sku'],
                    'image': product_data['image'],
                    'brand': brand,
                }
            )
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


def setup_periodic_tasks():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=6,
        period=IntervalSchedule.HOURS
    )
    for brand in Brand.objects.all():
        PeriodicTask.objects.create(
            interval=schedule,
            name=f'Update {brand.name} Products',
            task='products.tasks.update_products_for_brand',
            args=json.dumps([brand.id])
        )

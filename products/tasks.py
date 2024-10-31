from celery import shared_task
from .models import Brand, Product
from .scraper import scrape_amazon_products
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.core.exceptions import ObjectDoesNotExist
import json
import logging

logger = logging.getLogger('celery')


@shared_task(bind=True, max_retries=3)
def update_products_for_brand(self, brand_id):
    try:
        brand = Brand.objects.get(id=brand_id)
        logger.info(f"Starting scraping task for brand: {brand.name}")
        products = scrape_amazon_products(brand.name)
        if not products:
            logger.warning(f"No products found for brand: {brand.name}")

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
            if created:
                logger.info(f"Added new product: {product_data['name']}")
            else:
                logger.info(f"Updated product: {product_data['name']}")
        logger.info(f"Completed scraping task for brand: {brand.name}")
    except Brand.DoesNotExist:
        logger.error(f"Brand with id {brand_id} does not exist.")
    except Exception as exc:
        logger.error(f"Error in scraping task for brand {brand_id}: {exc}")
        self.retry(exc=exc, countdown=60)


def setup_periodic_tasks():
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=6,
        period=IntervalSchedule.HOURS
    )
    for brand in Brand.objects.all():
        task_name = f'Update {brand.name} Products'
        try:
            PeriodicTask.objects.get(name=task_name)
            logger.info(f"Periodic task '{task_name}' already exists.")
        except ObjectDoesNotExist:
            PeriodicTask.objects.create(
                interval=schedule,
                name=task_name,
                task='products.tasks.update_products_for_brand',
                args=json.dumps([brand.id])
            )
            logger.info(f"Created periodic task '{task_name}' for brand {brand.name}")

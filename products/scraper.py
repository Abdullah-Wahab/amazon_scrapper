import requests
from bs4 import BeautifulSoup
import random
import time

HEADERS = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'},
]


def scrape_amazon_products(brand_name):
    url = f'https://www.amazon.com/s?k={brand_name}'
    response = requests.get(url, headers=random.choice(HEADERS))

    if response.status_code != 200:
        raise Exception("Failed to load page")

    soup = BeautifulSoup(response.content, 'html.parser')
    products = []

    for item in soup.select('.s-result-item'):
        name = item.select_one('h2 span')
        asin = item.get('data-asin')
        image = item.select_one('.s-image')['src']

        if name and asin:
            products.append({
                'name': name.text,
                'asin': asin,
                'sku': None,  # SKU might not be available
                'image': image
            })
    return products

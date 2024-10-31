import requests
from bs4 import BeautifulSoup
import random
import time
import logging

logger = logging.getLogger('scraper')

HEADERS = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/536.36',
        'Accept-Language': 'en-US,en;q=0.5'}
]


def scrape_amazon_products(brand_name):
    products = []
    page = 1
    base_url = 'https://www.amazon.com/s'

    while True:
        print(f"Scraping page {page}")
        params = {'k': brand_name, 'page': page}
        response = requests.get(base_url, headers=random.choice(HEADERS), params=params)

        if response.status_code != 200:
            logger.error(f"Failed to load page: {response.status_code}")
            raise Exception("Failed to load page")

        # Parse the page content
        soup = BeautifulSoup(response.content, 'html.parser')
        page_products = parse_product_list(soup)

        if not page_products:
            logger.info("No more products found, ending scraping.")
            break

        products.extend(page_products)

        # Random delay avoiding detection
        time.sleep(random.uniform(1, 3))

        # Move to the next page
        page += 1

    return products


def parse_product_list(soup):
    products = []
    for item in soup.select('.s-result-item'):
        name_tag = item.select_one('h2 span')
        asin = item.get('data-asin')
        image_tag = item.select_one('.s-image')

        image = image_tag['src'] if image_tag else "No image available"
        sku = None

        if name_tag and asin:
            sku = fetch_product_sku(asin)
            products.append({
                'name': name_tag.text.strip(),
                'asin': asin,
                'sku': sku,
                'image': image
            })
            logger.debug(f"Scraped product: {name_tag.text.strip()}, ASIN: {asin}")

    return products


def fetch_product_sku(asin):
    product_url = f'https://www.amazon.com/dp/{asin}'
    try:
        product_response = requests.get(product_url, headers=random.choice(HEADERS))

        if product_response.status_code != 200 or "captcha" in product_response.url:
            logger.warning(f"Failed to load product page for ASIN {asin}")
            return None

        product_soup = BeautifulSoup(product_response.content, 'html.parser')
        sku_tag = product_soup.select_one('#sku')

        if sku_tag:
            return sku_tag.text.strip()
        else:
            print("SKU not found for ASIN", asin)
            return None
    except requests.RequestException as e:
        logger.error(f"Error fetching product page for ASIN {asin}: {e}")
        return None

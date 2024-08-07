import requests
from bs4 import BeautifulSoup
import random
import time
import re
from requests.exceptions import RequestException

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def fetch_html_content(url, max_retries=3, backoff_factor=0.3):
    headers = {
        "User-Agent": get_random_user_agent(),
        "Accept-Language": "en-US,en;q=0.9"
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                print(f"Successfully fetched HTML content from {url}")
                return response.text
            else:
                print(f"Failed to retrieve page: {response.status_code}")
        except RequestException as e:
            print(f"Connection error: {e}")

        time.sleep(backoff_factor * (2 ** attempt))

    return None

def parse_deals(html):
    soup = BeautifulSoup(html, 'html.parser')
    deals = []

    for item in soup.select('.elementor-widget-wrap'):
        image_element = item.select_one('img.attachment-large')
        price_element = item.select_one('.elementor-element-242102ba h2')
        discount_element = item.select_one('.elementor-element-3ddfc4ce h2')
        title_element = item.select_one('.elementor-element-267f52eb h2')
        product_link_element = item.select_one('a.elementor-button-link')

        if not all([image_element, price_element, discount_element, title_element, product_link_element]):
            continue

        image_url = image_element['src']
        price_text = price_element.get_text(strip=True)
        discount_text = discount_element.get_text(strip=True)
        title = title_element.get_text(strip=True)
        product_link = product_link_element['href']

        promo_code_match = re.search(r'code: (\w+)', discount_text)
        promo_code = promo_code_match.group(1) if promo_code_match else "No promo code"
        
        discount_parts = re.findall(r'\d+%', discount_text)
        discount = ', '.join(discount_parts) if discount_parts else "No discount"
        
        price_parts = re.findall(r'\d+\.\d+', price_text)
        if len(price_parts) == 2:
            sale_price, regular_price = map(float, price_parts)
        else:
            regular_price = sale_price = float(price_parts[0]) if price_parts else 0.0

        deal = {
            "title": title,
            "regular_price": f"${regular_price:.2f}",
            "price": f"${sale_price:.2f}",
            "promo_discount": discount,
            "promo_code": promo_code,
            "image": image_url,
            "product_link": product_link,
        }
        deals.append(deal)
        print(f"Parsed deal: {deal}")
        if len(deals) >= 10:
            break

    return deals

def fetch_deals_from_onlineatthelake():
    url = "https://onlineatthelake.com"
    html = fetch_html_content(url)
    if html:
        return parse_deals(html)
    else:
        print("Failed to fetch or parse deals from onlineatthelake")
        return []

def fetch_deals_from_gingerpenny():
    url = "https://gingerpenny.com"
    html = fetch_html_content(url)
    if html:
        return parse_deals(html)
    else:
        print("Failed to fetch or parse deals from gingerpenny")
        return []

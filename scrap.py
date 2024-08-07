# web.py

import requests
from bs4 import BeautifulSoup
import random
import time
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

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
                return response.text
            else:
                print(f"Failed to retrieve page: {response.status_code}")
        except RequestException as e:
            print(f"Connection error: {e}")

        time.sleep(backoff_factor * (2 ** attempt))

    return None

def fetch_html_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(5)

    html_content = driver.page_source
    driver.quit()

    return html_content

def parse_onlineatthelake_deals(html):
    soup = BeautifulSoup(html, 'html.parser')
    deals = []

    for item in soup.find_all('div', class_='elementor-column'):
        title_element_container = item.find('div', class_='elementor-element-609c1fb')
        price_element_container = item.find('div', class_='elementor-element-6c132b23')
        discount_element_container = item.find('div', class_='elementor-element-378d8a4b')
        image_element = item.find('img', class_='attachment-large')
        product_link_element = item.find('a', class_='elementor-button-link')

        if not all([title_element_container, price_element_container, discount_element_container, image_element, product_link_element]):
            continue

        title_element = title_element_container.find('h2', class_='elementor-heading-title')
        price_element = price_element_container.find('h2', class_='elementor-heading-title')
        discount_element = discount_element_container.find('h2', class_='elementor-heading-title')

        if not all([title_element, price_element, discount_element]):
            continue

        title = title_element.text.strip()
        price_text = price_element.text.strip().split('(')[0].strip()
        regular_price, sale_price = map(float, price_text.split('-'))
        promo_code = discount_element.text.strip().split(':')[-1].strip()
        image_url = image_element['src']
        product_link = product_link_element['href']

        deal = {
            "title": title,
            "regular_price": f"${max(regular_price, sale_price):.2f}",
            "price": f"${min(regular_price, sale_price):.2f}",
            "promo_code": promo_code,
            "discount": discount_element.text.strip(),
            "image": image_url,
            "product_link": product_link,
        }
        deals.append(deal)
        if len(deals) >= 10:
            break

    return deals

def fetch_deals_from_onlineatthelake():
    url = "https://onlineatthelake.com"
    html = fetch_html_content(url)
    return parse_onlineatthelake_deals(html)

# Example of another fetching function
def fetch_deals_from_gingerpenny():
    url = "https://gingerpenny.com"
    html = fetch_html_content(url)
    return parse_onlineatthelake_deals(html)

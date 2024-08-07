import requests
from bs4 import BeautifulSoup

def scrape_marketplace():
    url = 'https://www.facebook.com/marketplace'
    headers = {
        'User-Agent': 'Your User-Agent',
        'cookie': 'Your Cookie Here'  # Replace with your actual cookie
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    items = extract_data(soup)
    return items

def extract_data(soup):
    items = []
    for item in soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24'):
        try:
            title = item.find('span', class_='x1lliihq x1iyjqo2').text.strip()
            price = item.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u').text.strip()
            location = item.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u').text.strip()
            link = 'https://www.facebook.com' + item.find('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv')['href']
            image_url = item.find('img', class_='xt7dq6l xl1xv1r x6ikm8r x10wlt62 xh8yej3')['src']
            items.append({'title': title, 'price': price, 'location': location, 'link': link, 'image_url': image_url})
        except AttributeError:
            continue
    return items

if __name__ == "__main__":
    items = scrape_marketplace()
    for item in items:
        print(f"Title: {item['title']}, Price: {item['price']}, Location: {item['location']}, Link: {item['link']}, Image URL: {item['image_url']}")

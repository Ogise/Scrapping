import time
import requests
from web import fetch_deals_from_onlineatthelake, fetch_deals_from_gingerpenny

SERVER_URL = "http://localhost:5000/add_deal"

def send_deal_to_server(deal):
    try:
        response = requests.post(SERVER_URL, json=deal)
        response.raise_for_status()
        print("Deal successfully sent to server.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send deal to server: {e}")

if __name__ == "__main__":
    websites = [
        fetch_deals_from_onlineatthelake,
        fetch_deals_from_gingerpenny,
    ]

    for fetch_deals in websites:
        deals = fetch_deals()
        for deal in deals:
            send_deal_to_server(deal)
            time.sleep(1)  # Sleep to avoid hitting rate limits

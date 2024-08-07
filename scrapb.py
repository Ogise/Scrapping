import time
import requests
from scrap import fetch_deals_from_onlineatthelake, fetch_deals_from_gingerpenny

DISCORD_WEBHOOK_URLS = {
    "deals": "https://discord.com/api/webhooks/1252370186988949586/iORx5E-rnUZL6uFIcahiqsbKOadaBQB3Yf3hoECV1xfGwyhBP1SCtBwjbJ2jHKIi7f1x"  # Replace with your actual Discord webhook URL
}

def send_deal_to_discord(deal, channel):
    if channel not in DISCORD_WEBHOOK_URLS:
        print(f"Webhook URL not found for channel {channel}. Skipping.")
        return

    webhook_url = DISCORD_WEBHOOK_URLS[channel]

    description = (
        f"**Regular Price:** {deal['regular_price']}\n"
        f"**Price:** {deal['price']}\n"
        f"**Promo Code:** {deal['promo_code']}\n"
    )

    discord_payload = {
        "username": "Deals Bot",
        "avatar_url": "https://example.com/avatar.png",  # Replace with your avatar URL if needed
        "embeds": [
            {
                "title": deal["title"],
                "url": deal["product_link"],
                "description": description,
                "image": {
                    "url": deal["image"]
                },
                "footer": {
                    "text": "Click the title to buy the product!"
                },
                "fields": [
                    {
                        "name": "Discount",
                        "value": deal["discount"],
                        "inline": False
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=discord_payload)
        response.raise_for_status()
        print(f"Deal successfully sent to {channel} channel.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send deal to Discord: {e}")
        if hasattr(e, 'response') and e.response.status_code == 405:
            print("Check if the webhook URL allows POST requests.")
        elif hasattr(e, 'response') and e.response.status_code == 429:
            print(f"Rate limited by Discord. Retry after {e.response.headers['Retry-After']} seconds.")
        else:
            print("Unexpected error occurred, not retrying.")

if __name__ == "__main__":
    websites = [
        fetch_deals_from_onlineatthelake,
        fetch_deals_from_gingerpenny,
    ]

    for fetch_deals in websites:
        deals = fetch_deals()
        for deal in deals:
            send_deal_to_discord(deal, "deals")
            time.sleep(1)  # Sleep to avoid hitting rate limits

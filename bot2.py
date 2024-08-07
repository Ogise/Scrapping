import time
import requests
from web2 import scrape_marketplace

DISCORD_WEBHOOK_URLS = {
    "marketplace": "https://discord.com/api/webhooks/1252370186988949586/iORx5E-rnUZL6uFIcahiqsbKOadaBQB3Yf3hoECV1xfGwyhBP1SCtBwjbJ2jHKIi7f1x"  # Replace with your actual Discord webhook URL
}

def send_item_to_discord(item, channel):
    if channel not in DISCORD_WEBHOOK_URLS:
        print(f"Webhook URL not found for channel {channel}. Skipping.")
        return

    webhook_url = DISCORD_WEBHOOK_URLS[channel]

    description = (
        f"**Price:** {item['price']}\n"
        f"**Location:** {item['location']}\n"
        f"**Image:** {item['image_url']}\n"
        f"[Click here to view]({item['link']})"
    )

    discord_payload = {
        "username": "Marketplace Bot",
        "avatar_url": "https://example.com/avatar.png",  # Replace with your avatar URL if needed
        "embeds": [
            {
                "title": item["title"],
                "url": item["link"],
                "description": description,
                "image": {
                    "url": item["image_url"]
                },
                "footer": {
                    "text": "Click the title to view the item!"
                }
            }
        ]
    }

    try:
        response = requests.post(webhook_url, json=discord_payload)
        response.raise_for_status()
        print(f"Item successfully sent to {channel} channel: {item['title']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send item to Discord: {e}")
        if hasattr(e, 'response') and e.response.status_code == 405:
            print("Check if the webhook URL allows POST requests.")
        elif hasattr(e, 'response') and e.response.status_code == 429:
            print(f"Rate limited by Discord. Retry after {e.response.headers['Retry-After']} seconds.")
        else:
            print("Unexpected error occurred, not retrying.")

if __name__ == "__main__":
    items = scrape_marketplace()
    if not items:
        print("No items found.")
    for item in items:
        send_item_to_discord(item, "marketplace")
        time.sleep(1)  # Sleep to avoid hitting rate limits

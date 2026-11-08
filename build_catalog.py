import urllib.request
import json
import os

token = "9120376953:AAG7xxKbAQDZISNyAxZpS1Qp-PD6Eo_MDRw"
packs = ["RestrictedEmoji", "TgAndroidIcons", "tgmacicons", "PremiumBadges", "StarEmoji"]

catalog = {
    "by_emoji": {},      # unicode emoji -> {"custom_emoji_id": id, "pack": pack}
    "categories": {},    # category name -> list of {"emoji": e, "id": id, "name": n}
    "keywords": {}       # keyword -> list of {emoji, id}
}

print("Fetching emoji packs from Telegram Bot API...")
for pack_name in packs:
    try:
        url = f"https://api.telegram.org/bot{token}/getStickerSet?name={pack_name}"
        req = urllib.request.Request(url, headers={"User-Agent": "TelegramBot/1.0"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            if data.get("ok"):
                stickers = data["result"].get("stickers", [])
                print(f"Pack {pack_name}: {len(stickers)} stickers found.")
                for s in stickers:
                    e = s.get("emoji")
                    cid = s.get("custom_emoji_id")
                    if e and cid:
                        # Prefer RestrictedEmoji or TgAndroidIcons
                        if e not in catalog["by_emoji"] or pack_name == "RestrictedEmoji":
                            catalog["by_emoji"][e] = {
                                "custom_emoji_id": cid,
                                "fallback": e,
                                "pack": pack_name
                            }
    except Exception as ex:
        print(f"Error fetching {pack_name}: {ex}")

print(f"Total unique emojis mapped: {len(catalog['by_emoji'])}")

# Save to emoji_catalog.json
with open("emoji_catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print("Saved emoji_catalog.json successfully!")


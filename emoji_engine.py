import html
import re
import json
import os
import string
from typing import Dict, Any, List, Optional, Tuple

CATALOG_PATH = os.path.join(os.path.dirname(__file__), "emoji_catalog.json")
USER_FAV_PATH = os.path.join(os.path.dirname(__file__), "user_favorite_packs.json")
CHANNEL_FAV_PATH = os.path.join(os.path.dirname(__file__), "user_channel_packs.json")

# Load catalogs
_CATALOG: Dict[str, Any] = {}
if os.path.exists(CATALOG_PATH):
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            _CATALOG = json.load(f).get("by_emoji", {})
    except Exception as e:
        print(f"Error loading catalog: {e}")

_USER_FAV: Dict[str, Any] = {}
if os.path.exists(USER_FAV_PATH):
    try:
        with open(USER_FAV_PATH, "r", encoding="utf-8") as f:
            _USER_FAV = json.load(f)
    except Exception as e:
        print(f"Error loading user fav: {e}")

_CHANNEL_FAV: Dict[str, Any] = {}
if os.path.exists(CHANNEL_FAV_PATH):
    try:
        with open(CHANNEL_FAV_PATH, "r", encoding="utf-8") as f:
            _CHANNEL_FAV = json.load(f)
    except Exception as e:
        print(f"Error loading channel fav: {e}")

# LED Screen letters & numbers (LedScreenEmoji)
LED_LETTERS: Dict[str, str] = {}
LED_NUMBERS: Dict[str, str] = {}
if "LedScreenEmoji" in _USER_FAV:
    led_stk = _USER_FAV["LedScreenEmoji"].get("stickers", [])
    for i, ch in enumerate(string.ascii_uppercase):
        if i < len(led_stk):
            LED_LETTERS[ch] = led_stk[i]["custom_emoji_id"]
    for d in range(10):
        idx = 27 + d
        if idx < len(led_stk):
            LED_NUMBERS[str(d)] = led_stk[idx]["custom_emoji_id"]

# Retro Font letters & numbers (RetroFontEmoji)
RETRO_LETTERS: Dict[str, str] = {}
RETRO_NUMBERS: Dict[str, str] = {}
if "RetroFontEmoji" in _USER_FAV:
    ret_stk = _USER_FAV["RetroFontEmoji"].get("stickers", [])
    for i, ch in enumerate(string.ascii_uppercase):
        if i < len(ret_stk):
            RETRO_LETTERS[ch] = ret_stk[i]["custom_emoji_id"]
    for d in range(1, 10):
        idx = 25 + d
        if idx < len(ret_stk):
            RETRO_NUMBERS[str(d)] = ret_stk[idx]["custom_emoji_id"]
    if len(ret_stk) > 35:
        RETRO_NUMBERS["0"] = ret_stk[35]["custom_emoji_id"]

# Cat Font letters & numbers (CatFontEmoji)
CAT_LETTERS: Dict[str, str] = {}
CAT_NUMBERS: Dict[str, str] = {}
if "CatFontEmoji" in _USER_FAV:
    cat_stk = _USER_FAV["CatFontEmoji"].get("stickers", [])
    for i, ch in enumerate(string.ascii_uppercase):
        if i < len(cat_stk):
            CAT_LETTERS[ch] = cat_stk[i]["custom_emoji_id"]
    for d in range(10):
        idx = 26 + d
        if idx < len(cat_stk):
            CAT_NUMBERS[str(d)] = cat_stk[idx]["custom_emoji_id"]

# Core Verified Badges
TAG_RED_VERIFIED = '<tg-emoji emoji-id="5992524725715209996">🔴</tg-emoji>'
TAG_BLUE_VERIFIED = '<tg-emoji emoji-id="5411309092427834175">✅</tg-emoji>'
TAG_GREEN_VERIFIED = '<tg-emoji emoji-id="5843482308207709657">✔️</tg-emoji>'

# XtremistQFS Badges (@XtremistQFS)
TAG_XTREMIST_BLUE = '<tg-emoji emoji-id="6267313108360895894">✅</tg-emoji>'
TAG_XTREMIST_CHECK = '<tg-emoji emoji-id="6267110175451126193">✔️</tg-emoji>'
TAG_XTREMIST_STAR = '<tg-emoji emoji-id="6264872282741546463">⭐️</tg-emoji>'
TAG_XTREMIST_GLOW = '<tg-emoji emoji-id="6267099742975565602">✅</tg-emoji>'

# Emoji_hasib_by_fStikBot Badges
TAG_HASIB_VERIFIED = '<tg-emoji emoji-id="6271390196260937507">✅</tg-emoji>'
TAG_HASIB_GOLD = '<tg-emoji emoji-id="6271518860596222353">🥇</tg-emoji>'
TAG_HASIB_SHIELD = '<tg-emoji emoji-id="6271371418663917390">🛡</tg-emoji>'
TAG_HASIB_DOWN = '<tg-emoji emoji-id="6271603750624827280">⬇️</tg-emoji>'
TAG_HASIB_FIRE = '<tg-emoji emoji-id="6271767049576388352">🔥</tg-emoji>'
TAG_HASIB_MONEY = '<tg-emoji emoji-id="6271636452505820776">💰</tg-emoji>'
TAG_HASIB_PIN = '<tg-emoji emoji-id="6271683469512808965">📌</tg-emoji>'
TAG_HASIB_ROCKET = '<tg-emoji emoji-id="6271710459087297021">🚀</tg-emoji>'
TAG_HASIB_HUNDRED = '<tg-emoji emoji-id="6271738810166418011">💯</tg-emoji>'
TAG_HASIB_SIREN = '<tg-emoji emoji-id="6271526381083957527">🚨</tg-emoji>'
TAG_HASIB_ID = '<tg-emoji emoji-id="6271604235956131941">🪪</tg-emoji>'

# stickerXtara & tarahume Badges (@stickerXtara @tarahume)
TAG_TARA_LIGHTNING = '<tg-emoji emoji-id="6271656548657795731">⚡️</tg-emoji>'
TAG_TARA_LIGHTNING2 = '<tg-emoji emoji-id="6271263782488510976">⚡️</tg-emoji>'
TAG_TARA_LIGHTNING3 = '<tg-emoji emoji-id="6269322362781439325">⚡️</tg-emoji>'

# OrderEmoji Badges (@OrderEmoji)
TAG_ORDER_STAR = '<tg-emoji emoji-id="5355033944129552118">🌟</tg-emoji>'
TAG_ORDER_STAR2 = '<tg-emoji emoji-id="5354929932906546194">🌟</tg-emoji>'
TAG_ORDER_STAR3 = '<tg-emoji emoji-id="5355169587786695299">🌟</tg-emoji>'

# Additional Premium Badges
TAG_CROWN = '<tg-emoji emoji-id="5467406098367521267">👑</tg-emoji>'
TAG_DIAMOND = '<tg-emoji emoji-id="5471952986970267163">💎</tg-emoji>'
TAG_HEART = '<tg-emoji emoji-id="5449505950283078474">❤️</tg-emoji>'
TAG_ROSE = '<tg-emoji emoji-id="5440911110838425969">🌹</tg-emoji>'
TAG_SPARKLES = '<tg-emoji emoji-id="5472164874886846699">✨</tg-emoji>'
TAG_HAND_WAVE = '<tg-emoji emoji-id="5875465628285931233">👋</tg-emoji>'
TAG_POINT_DOWN = '<tg-emoji emoji-id="5470177992950946662">👇</tg-emoji>'
TAG_POINT_RIGHT = '<tg-emoji emoji-id="5471978009449731768">👉</tg-emoji>'

def to_led_screen(text: str) -> str:
    """Converts English letters and numbers into user-favorite LED Screen emojis."""
    res = []
    for ch in text.upper():
        if ch in LED_LETTERS:
            res.append(f'<tg-emoji emoji-id="{LED_LETTERS[ch]}">🔠</tg-emoji>')
        elif ch in LED_NUMBERS:
            res.append(f'<tg-emoji emoji-id="{LED_NUMBERS[ch]}">{ch}️⃣</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def to_retro_font(text: str) -> str:
    """Converts English letters and numbers into user-favorite Retro Font emojis."""
    res = []
    for ch in text.upper():
        if ch in RETRO_LETTERS:
            res.append(f'<tg-emoji emoji-id="{RETRO_LETTERS[ch]}">🔤</tg-emoji>')
        elif ch in RETRO_NUMBERS:
            res.append(f'<tg-emoji emoji-id="{RETRO_NUMBERS[ch]}">{ch}️⃣</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def to_cat_font(text: str) -> str:
    """Converts English letters and numbers into user-favorite Cat Font emojis."""
    res = []
    for ch in text.upper():
        if ch in CAT_LETTERS:
            res.append(f'<tg-emoji emoji-id="{CAT_LETTERS[ch]}">🔠</tg-emoji>')
        elif ch in CAT_NUMBERS:
            res.append(f'<tg-emoji emoji-id="{CAT_NUMBERS[ch]}">{ch}️⃣</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def convert_digits_to_led(text: str) -> str:
    """Replaces digits 0-9 in text with LED Screen number emojis."""
    def rep(m):
        d = m.group(0)
        if d in LED_NUMBERS:
            return f'<tg-emoji emoji-id="{LED_NUMBERS[d]}">{d}️⃣</tg-emoji>'
        return d
    return re.sub(r'\d', rep, text)

def convert_existing_emojis_to_premium(text: str) -> str:
    """Converts standard unicode emojis into premium custom emoji tags."""
    emoji_pattern = re.compile(
        "["
        "\U0001F1E0-\U0001F1FF"
        "\U0001F300-\U0001F5FF"
        "\U0001F600-\U0001F64F"
        "\U0001F680-\U0001F6FF"
        "\U0001F700-\U0001F77F"
        "\U0001F780-\U0001F7FF"
        "\U0001F800-\U0001F8FF"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U00002600-\U000026FF"
        "]+",
        flags=re.UNICODE
    )

    def replace_match(match):
        em = match.group(0)
        if em == "🔥": return TAG_HASIB_FIRE
        if em in ["⚡️", "⚡"]: return TAG_TARA_LIGHTNING
        if em in ["⭐", "⭐️"]: return TAG_ORDER_STAR
        if em == "✅": return TAG_BLUE_VERIFIED
        if em == "✔️": return TAG_GREEN_VERIFIED
        if em == "🔴": return TAG_RED_VERIFIED
        if em == "🛡": return TAG_HASIB_SHIELD
        if em == "🥇": return TAG_HASIB_GOLD
        if em == "💰": return TAG_HASIB_MONEY
        if em == "📌": return TAG_HASIB_PIN
        if em == "⬇️": return TAG_HASIB_DOWN
        if em == "💯": return TAG_HASIB_HUNDRED

        if em in _CATALOG:
            cid = _CATALOG[em]["custom_emoji_id"]
            return f'<tg-emoji emoji-id="{cid}">{em}</tg-emoji>'
        return em

    return emoji_pattern.sub(replace_match, text)

# 1. LED Screen Style (from LedScreenEmoji)
def style_led(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))
        if is_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            led_text = to_led_screen(line_clean)
            if i == 0:
                escaped = f"{TAG_HASIB_FIRE} {led_text} {TAG_HASIB_FIRE}"
            else:
                escaped = f"<blockquote>{TAG_BLUE_VERIFIED} {led_text}</blockquote>"
        else:
            escaped = convert_digits_to_led(escaped)
            def rep_w(m):
                w = m.group(0)
                if len(w) <= 8 and w.isupper():
                    return to_led_screen(w)
                return w
            escaped = re.sub(r'\b[A-Z]{3,8}\b', rep_w, escaped)

            if i == 0 and len(lines) > 1:
                escaped = f"{TAG_HASIB_FIRE} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_HASIB_FIRE}"
            elif line_clean.startswith("@") or "submit" in line_clean.lower() or "file" in line_clean.lower():
                escaped = f"<blockquote>{TAG_HASIB_DOWN} {escaped}</blockquote>"
            else:
                badges = [TAG_BLUE_VERIFIED, TAG_GREEN_VERIFIED, TAG_RED_VERIFIED, TAG_HASIB_SHIELD, TAG_HASIB_GOLD]
                badge = badges[i % len(badges)]
                escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 2. Retro Font Style (from RetroFontEmoji)
def style_retro(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))
        if is_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            ret_text = to_retro_font(line_clean)
            if i == 0:
                escaped = f"{TAG_HASIB_FIRE} {ret_text} {TAG_HASIB_FIRE}"
            else:
                escaped = f"<blockquote>{TAG_XTREMIST_BLUE} {ret_text}</blockquote>"
        else:
            def rep_num(m):
                d = m.group(0)
                if d in RETRO_NUMBERS:
                    return f'<tg-emoji emoji-id="{RETRO_NUMBERS[d]}">{d}️⃣</tg-emoji>'
                return d
            escaped = re.sub(r'\d', rep_num, escaped)
            def rep_w(m):
                w = m.group(0)
                if len(w) <= 8 and w.isupper():
                    return to_retro_font(w)
                return w
            escaped = re.sub(r'\b[A-Z]{3,8}\b', rep_w, escaped)

            if i == 0 and len(lines) > 1:
                escaped = f"{TAG_CROWN} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_DIAMOND}"
            else:
                badges = [TAG_RED_VERIFIED, TAG_BLUE_VERIFIED, TAG_XTREMIST_BLUE, TAG_HASIB_GOLD]
                badge = badges[i % len(badges)]
                escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 3. Cat Font Style (from CatFontEmoji)
def style_cat(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))
        if is_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            cat_text = to_cat_font(line_clean)
            escaped = f"<blockquote>{TAG_HEART} {cat_text} {TAG_SPARKLES}</blockquote>"
        else:
            def rep_cat_num(m):
                d = m.group(0)
                if d in CAT_NUMBERS:
                    return f'<tg-emoji emoji-id="{CAT_NUMBERS[d]}">{d}️⃣</tg-emoji>'
                return d
            escaped = re.sub(r'\d', rep_cat_num, escaped)
            if i == 0:
                escaped = f"{TAG_HEART} {TAG_SPARKLES} <b>{escaped}</b> {TAG_ROSE} {TAG_HEART}"
            else:
                escaped = f"<blockquote>{TAG_HEART} {escaped} {TAG_BLUE_VERIFIED}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 4. Hasib Verified Pack Style (from Emoji_hasib_by_fStikBot + RedVerified)
def style_hasib(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    hasib_badges = [TAG_RED_VERIFIED, TAG_HASIB_VERIFIED, TAG_HASIB_SHIELD, TAG_HASIB_GOLD, TAG_HASIB_PIN]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        escaped = convert_digits_to_led(escaped)
        badge = hasib_badges[i % len(hasib_badges)]
        if i == 0:
            escaped = f"{TAG_HASIB_FIRE} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_HASIB_VERIFIED} {TAG_HASIB_FIRE}"
        elif line_clean.startswith("@") or "submit" in line_clean.lower() or "file" in line_clean.lower():
            escaped = f"<blockquote>{TAG_HASIB_DOWN} {escaped}</blockquote>"
        else:
            escaped = f"<blockquote>{badge} {escaped} {TAG_HASIB_FIRE if i % 2 == 1 else ''}</blockquote>".strip()
        decorated.append(escaped)
    return "\n".join(decorated)

# 5. Xtremist Verified Style (from XtremistQFS)
def style_xtremist(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    xtremist_badges = [TAG_XTREMIST_BLUE, TAG_XTREMIST_CHECK, TAG_XTREMIST_GLOW, TAG_XTREMIST_STAR]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        escaped = convert_digits_to_led(escaped)
        badge = xtremist_badges[i % len(xtremist_badges)]
        if i == 0:
            escaped = f"{TAG_XTREMIST_STAR} {TAG_XTREMIST_BLUE} <b>{escaped}</b> {TAG_XTREMIST_GLOW} {TAG_XTREMIST_STAR}"
        else:
            escaped = f"<blockquote>{badge} {escaped} {TAG_XTREMIST_CHECK}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 6. Tara Lightning & Energy Style (from stickerXtara_by_fStikBot)
def style_tara(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    tara_badges = [TAG_TARA_LIGHTNING, TAG_TARA_LIGHTNING2, TAG_TARA_LIGHTNING3, TAG_HASIB_FIRE]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        escaped = convert_digits_to_led(escaped)
        badge = tara_badges[i % len(tara_badges)]
        if i == 0:
            escaped = f"{TAG_TARA_LIGHTNING} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_TARA_LIGHTNING}"
        else:
            escaped = f"<blockquote>{badge} {escaped} {TAG_TARA_LIGHTNING}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 7. Order Star Style (from OrderEmoji_by_fStikBot)
def style_order(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    order_badges = [TAG_ORDER_STAR, TAG_ORDER_STAR2, TAG_ORDER_STAR3, TAG_BLUE_VERIFIED]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        escaped = convert_digits_to_led(escaped)
        badge = order_badges[i % len(order_badges)]
        if i == 0:
            escaped = f"{TAG_ORDER_STAR} {TAG_CROWN} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_ORDER_STAR}"
        else:
            escaped = f"<blockquote>{badge} {escaped} {TAG_ORDER_STAR}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 8. Blockquote Multi-Verified Frame Style
def style_quotes(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    badges = [TAG_RED_VERIFIED, TAG_BLUE_VERIFIED, TAG_GREEN_VERIFIED, TAG_HASIB_SHIELD, TAG_HASIB_GOLD]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        escaped = convert_digits_to_led(escaped)
        badge = badges[i % len(badges)]
        if i == 0:
            escaped = f"{TAG_HASIB_FIRE} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_HASIB_FIRE}"
        elif line_clean.startswith("@") or "submit" in line_clean.lower() or "file" in line_clean.lower():
            escaped = f"<blockquote>{TAG_HASIB_DOWN} {escaped}</blockquote>"
        else:
            escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 9. Smart All-in-One Style
def style_smart(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        escaped = convert_digits_to_led(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_HASIB_FIRE} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_HASIB_FIRE}"
        else:
            badges = [TAG_BLUE_VERIFIED, TAG_GREEN_VERIFIED, TAG_RED_VERIFIED, TAG_HASIB_SHIELD]
            badge = badges[i % len(badges)]
            escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

def decorate_text(text: str, style: str = "led") -> str:
    """Main decoration entry point."""
    style = style.lower().strip()
    if style == "led":
        return style_led(text)
    elif style == "retro":
        return style_retro(text)
    elif style == "cat":
        return style_cat(text)
    elif style == "hasib":
        return style_hasib(text)
    elif style == "xtremist":
        return style_xtremist(text)
    elif style == "tara":
        return style_tara(text)
    elif style == "order":
        return style_order(text)
    elif style == "quotes":
        return style_quotes(text)
    else:
        return style_smart(text)

def get_plain_text_for_copy(text: str, style: str = "led") -> str:
    """Returns a clean plain text version with standard emojis for CopyTextButton."""
    decorated = decorate_text(text, style=style)
    # Strip HTML tags
    clean = re.sub(r'<tg-emoji[^>]*>(.*?)</tg-emoji>', r'\1', decorated)
    clean = re.sub(r'</?blockquote>', '', clean)
    clean = re.sub(r'</?[bi]>', '', clean)
    return html.unescape(clean)

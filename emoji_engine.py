import os
import json
import re
import html
import string
from typing import Dict, Any, List, Tuple

# Paths
BASE_DIR = os.path.dirname(__file__)
CATALOG_PATH = os.path.join(BASE_DIR, "emoji_catalog.json")
MAPPINGS_PATH = os.path.join(BASE_DIR, "all_extracted_mappings.json")
USER_FAV_PATH = os.path.join(BASE_DIR, "user_favorite_packs.json")
CHANNEL_FAV_PATH = os.path.join(BASE_DIR, "user_channel_packs.json")

# Load extracted mappings
_MAPS: Dict[str, Any] = {}
if os.path.exists(MAPPINGS_PATH):
    try:
        with open(MAPPINGS_PATH, "r", encoding="utf-8") as f:
            _MAPS = json.load(f)
    except Exception:
        pass

# Load base catalog
_CATALOG: Dict[str, str] = {}
if os.path.exists(CATALOG_PATH):
    try:
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            _CATALOG = json.load(f).get("by_emoji", {})
    except Exception:
        pass

# Load user packs
_USER_FAV: Dict[str, Any] = {}
if os.path.exists(USER_FAV_PATH):
    try:
        with open(USER_FAV_PATH, "r", encoding="utf-8") as f:
            _USER_FAV = json.load(f)
    except Exception:
        pass

# -------------------------------------------------------------
# FONT MAPPINGS
# -------------------------------------------------------------

# 1. LED Screen (LedScreenEmoji)
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

# 2. Retro Font (RetroFontEmoji)
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

# 3. Cat Font (CatFontEmoji)
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

# 4. Slime Font (SlimeFontEmoji)
SLIME_LETTERS: Dict[str, Tuple[str, str]] = _MAPS.get("slime", {}).get("letters", {})
SLIME_NUMBERS: Dict[str, Tuple[str, str]] = _MAPS.get("slime", {}).get("numbers", {})

# 5. 3D ABC Font (ABCEmoji)
ABC_LETTERS: Dict[str, Tuple[str, str]] = _MAPS.get("abc", {}).get("letters", {})
ABC_NUMBERS: Dict[str, Tuple[str, str]] = _MAPS.get("abc", {}).get("numbers", {})

# 6. Bony Skeleton Font (BonyFontEmoji)
BONY_LETTERS: Dict[str, Tuple[str, str]] = _MAPS.get("bony", {}).get("letters", {})
BONY_NUMBERS: Dict[str, Tuple[str, str]] = _MAPS.get("bony", {}).get("numbers", {})

# 7. Spooky Letters (SpookyLetters)
SPOOKY_LETTERS: Dict[str, Tuple[str, str]] = _MAPS.get("spooky", {}).get("letters", {})

# 8. Festive Flags (FestiveFlags)
FLAGS_LETTERS: Dict[str, Tuple[str, str]] = _MAPS.get("flags", {}).get("letters", {})
FLAGS_NUMBERS: Dict[str, Tuple[str, str]] = _MAPS.get("flags", {}).get("numbers", {})

# 9. Table Font (TableFontEmoji)
TABLE_LETTERS: Dict[str, Tuple[str, str]] = _MAPS.get("table", {}).get("letters", {})

# -------------------------------------------------------------
# CORE & PREMIUM BADGE TAGS
# -------------------------------------------------------------

# Verified Badges
TAG_RED_VERIFIED = '<tg-emoji emoji-id="5992524725715209996">🔴</tg-emoji>'
TAG_BLUE_VERIFIED = '<tg-emoji emoji-id="5411309092427834175">✅</tg-emoji>'
TAG_GREEN_VERIFIED = '<tg-emoji emoji-id="5843482308207709657">✔️</tg-emoji>'

# XtremistQFS Badges
TAG_XTREMIST_BLUE = '<tg-emoji emoji-id="6267313108360895894">✅</tg-emoji>'
TAG_XTREMIST_CHECK = '<tg-emoji emoji-id="6267110175451126193">✔️</tg-emoji>'
TAG_XTREMIST_STAR = '<tg-emoji emoji-id="6264872282741546463">⭐️</tg-emoji>'
TAG_XTREMIST_GLOW = '<tg-emoji emoji-id="6267099742975565602">✅</tg-emoji>'

# Emoji_hasib Badges
TAG_HASIB_VERIFIED = '<tg-emoji emoji-id="6271390196260937507">✅</tg-emoji>'
TAG_HASIB_GOLD = '<tg-emoji emoji-id="6271518860596222353">🥇</tg-emoji>'
TAG_HASIB_SHIELD = '<tg-emoji emoji-id="6271371418663917390">🛡</tg-emoji>'
TAG_HASIB_DOWN = '<tg-emoji emoji-id="6271603750624827280">⬇️</tg-emoji>'
TAG_HASIB_FIRE = '<tg-emoji emoji-id="6271767049576388352">🔥</tg-emoji>'
TAG_HASIB_MONEY = '<tg-emoji emoji-id="6271636452505820776">💰</tg-emoji>'
TAG_HASIB_PIN = '<tg-emoji emoji-id="6271683469512808965">📌</tg-emoji>'
TAG_HASIB_ROCKET = '<tg-emoji emoji-id="6271710459087297021">🚀</tg-emoji>'
TAG_HASIB_HUNDRED = '<tg-emoji emoji-id="6271738810166418011">💯</tg-emoji>'

# stickerXtara Badges
TAG_TARA_LIGHTNING = '<tg-emoji emoji-id="6271656548657795731">⚡️</tg-emoji>'
TAG_TARA_LIGHTNING2 = '<tg-emoji emoji-id="6271263782488510976">⚡️</tg-emoji>'
TAG_TARA_LIGHTNING3 = '<tg-emoji emoji-id="6269322362781439325">⚡️</tg-emoji>'

# OrderEmoji Badges
TAG_ORDER_STAR = '<tg-emoji emoji-id="5355033944129552118">🌟</tg-emoji>'
TAG_ORDER_STAR2 = '<tg-emoji emoji-id="5354929932906546194">🌟</tg-emoji>'

# AttractivePack Badges
TAG_ATTR_CHECK_BLUE = '<tg-emoji emoji-id="5208748315805499400">✅</tg-emoji>'
TAG_ATTR_CHECK_NEON = '<tg-emoji emoji-id="5211112665237175703">✅</tg-emoji>'
TAG_ATTR_CHECK_GOLD = '<tg-emoji emoji-id="5208727996315220567">✅</tg-emoji>'
TAG_ATTR_CHECK_GREEN = '<tg-emoji emoji-id="5208966130776948094">✅</tg-emoji>'
TAG_ATTR_BUTTON_BLUE = '<tg-emoji emoji-id="5210935111289159311">🔘</tg-emoji>'
TAG_ATTR_BUTTON_GOLD = '<tg-emoji emoji-id="5210708311246126137">🔘</tg-emoji>'
TAG_ATTR_BUTTON_GREEN = '<tg-emoji emoji-id="5208536350579506258">🔘</tg-emoji>'
TAG_ATTR_CIRCLE_BLUE = '<tg-emoji emoji-id="5208773600277970208">🔵</tg-emoji>'
TAG_ATTR_CIRCLE_GREEN = '<tg-emoji emoji-id="5211182849297762045">🟢</tg-emoji>'
TAG_ATTR_CIRCLE_RED = '<tg-emoji emoji-id="5208429100951159058">🔴</tg-emoji>'
TAG_ATTR_CIRCLE_YELLOW = '<tg-emoji emoji-id="5208447513475954676">🟡</tg-emoji>'
TAG_ATTR_LIGHTNING = '<tg-emoji emoji-id="5343528160535270636">⚡️</tg-emoji>'
TAG_ATTR_STAR = '<tg-emoji emoji-id="5413351005779672594">⭐️</tg-emoji>'

# DSPSIR Badges
TAG_DSPSIR_APPLE_GREEN = '<tg-emoji emoji-id="6271378634208974347">🍏</tg-emoji>'
TAG_DSPSIR_APPLE_GLOW = '<tg-emoji emoji-id="6273556792513402505">🍏</tg-emoji>'
TAG_DSPSIR_APPLE_NEON = '<tg-emoji emoji-id="6273972468038242731">🍏</tg-emoji>'
TAG_DSPSIR_CROWN = '<tg-emoji emoji-id="6269556155031228243">👑</tg-emoji>'
TAG_DSPSIR_DIAMOND = '<tg-emoji emoji-id="6271537028307881531">💎</tg-emoji>'
TAG_DSPSIR_MEDAL = '<tg-emoji emoji-id="6269400956387987689">🥇</tg-emoji>'
TAG_DSPSIR_CHECK_CYAN = '<tg-emoji emoji-id="6269116058322342852">✔️</tg-emoji>'
TAG_DSPSIR_CHECK_BLUE = '<tg-emoji emoji-id="6237651574588445185">✅</tg-emoji>'
TAG_DSPSIR_CARD = '<tg-emoji emoji-id="6129870117619634982">💳</tg-emoji>'
TAG_DSPSIR_LIGHTNING = '<tg-emoji emoji-id="6082519348721751560">⚡️</tg-emoji>'

# Electricshok12 Badges
TAG_ELEC_SHOCK1 = '<tg-emoji emoji-id="6323076240722891410">⚡️</tg-emoji>'
TAG_ELEC_SHOCK2 = '<tg-emoji emoji-id="6323138152676464326">⚡️</tg-emoji>'
TAG_ELEC_SHOCK3 = '<tg-emoji emoji-id="6323092089152213738">⚡️</tg-emoji>'
TAG_ELEC_SHOCK4 = '<tg-emoji emoji-id="6323458978143540451">⚡️</tg-emoji>'
TAG_ELEC_SHOCK5 = '<tg-emoji emoji-id="6323605131585656386">⚡️</tg-emoji>'

# Shuzi5 Badges
TAG_SHUZI_FIRE = '<tg-emoji emoji-id="6127438745223303339">🔥</tg-emoji>'
TAG_SHUZI_STAR = '<tg-emoji emoji-id="6127520306652254361">⭐</tg-emoji>'
TAG_SHUZI_DIAMOND = '<tg-emoji emoji-id="6127596907393978755">💎</tg-emoji>'
TAG_SHUZI_ROCKET = '<tg-emoji emoji-id="6129827464299417750">🚀</tg-emoji>'
TAG_SHUZI_HUNDRED = '<tg-emoji emoji-id="6127365528915809239">💯</tg-emoji>'
TAG_SHUZI_MONEY = '<tg-emoji emoji-id="6127269630886023130">💰</tg-emoji>'
TAG_SHUZI_CROWN = '<tg-emoji emoji-id="6127541064229196758">👑</tg-emoji>'
TAG_SHUZI_RAINBOW = '<tg-emoji emoji-id="6127540656207303208">🌈</tg-emoji>'

# Generic Premium Badges
TAG_CROWN = '<tg-emoji emoji-id="5467406098367521267">👑</tg-emoji>'
TAG_DIAMOND = '<tg-emoji emoji-id="5471952986970267163">💎</tg-emoji>'
TAG_HEART = '<tg-emoji emoji-id="5449505950283078474">❤️</tg-emoji>'
TAG_ROSE = '<tg-emoji emoji-id="5440911110838425969">🌹</tg-emoji>'
TAG_SPARKLES = '<tg-emoji emoji-id="5472164874886846699">✨</tg-emoji>'
TAG_HAND_WAVE = '<tg-emoji emoji-id="5875465628285931233">👋</tg-emoji>'
TAG_POINT_DOWN = '<tg-emoji emoji-id="5470177992950946662">👇</tg-emoji>'
TAG_POINT_RIGHT = '<tg-emoji emoji-id="5471978009449731768">👉</tg-emoji>'

# -------------------------------------------------------------
# FONT HELPER FUNCTIONS
# -------------------------------------------------------------

def to_led_screen(text: str) -> str:
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
    res = []
    for ch in text.upper():
        if ch in CAT_LETTERS:
            res.append(f'<tg-emoji emoji-id="{CAT_LETTERS[ch]}">🔠</tg-emoji>')
        elif ch in CAT_NUMBERS:
            res.append(f'<tg-emoji emoji-id="{CAT_NUMBERS[ch]}">{ch}️⃣</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def to_slime_font(text: str) -> str:
    res = []
    for ch in text.upper():
        if ch in SLIME_LETTERS:
            cid, fb = SLIME_LETTERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        elif ch in SLIME_NUMBERS:
            cid, fb = SLIME_NUMBERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def to_abc_font(text: str) -> str:
    res = []
    for ch in text.upper():
        if ch in ABC_LETTERS:
            cid, fb = ABC_LETTERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        elif ch in ABC_NUMBERS:
            cid, fb = ABC_NUMBERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def to_bony_font(text: str) -> str:
    res = []
    for ch in text.upper():
        if ch in BONY_LETTERS:
            cid, fb = BONY_LETTERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        elif ch in BONY_NUMBERS:
            cid, fb = BONY_NUMBERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def to_spooky_font(text: str) -> str:
    res = []
    for ch in text.upper():
        if ch in SPOOKY_LETTERS:
            cid, fb = SPOOKY_LETTERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def to_flags_font(text: str) -> str:
    res = []
    for ch in text.upper():
        if ch in FLAGS_LETTERS:
            cid, fb = FLAGS_LETTERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        elif ch in FLAGS_NUMBERS:
            cid, fb = FLAGS_NUMBERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def to_table_font(text: str) -> str:
    res = []
    for ch in text.upper():
        if ch in TABLE_LETTERS:
            cid, fb = TABLE_LETTERS[ch]
            res.append(f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>')
        else:
            res.append(ch)
    return "".join(res)

def convert_existing_emojis_to_premium(text: str) -> str:
    def rep(m):
        em = m.group(0)
        if em in _CATALOG:
            return f'<tg-emoji emoji-id="{_CATALOG[em]}">{em}</tg-emoji>'
        return em
    return re.sub(r'[\U00010000-\U0010ffff]', rep, text)

def convert_digits_to_led(text: str) -> str:
    def rep(m):
        d = m.group(0)
        if d in LED_NUMBERS:
            return f'<tg-emoji emoji-id="{LED_NUMBERS[d]}">{d}️⃣</tg-emoji>'
        return d
    return re.sub(r'\d', rep, text)

def convert_digits_to_abc(text: str) -> str:
    def rep(m):
        d = m.group(0)
        if d in ABC_NUMBERS:
            cid, fb = ABC_NUMBERS[d]
            return f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>'
        return d
    return re.sub(r'\d', rep, text)

def convert_digits_to_slime(text: str) -> str:
    def rep(m):
        d = m.group(0)
        if d in SLIME_NUMBERS:
            cid, fb = SLIME_NUMBERS[d]
            return f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>'
        return d
    return re.sub(r'\d', rep, text)

def convert_digits_to_bony(text: str) -> str:
    def rep(m):
        d = m.group(0)
        if d in BONY_NUMBERS:
            cid, fb = BONY_NUMBERS[d]
            return f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>'
        return d
    return re.sub(r'\d', rep, text)

def convert_digits_to_flags(text: str) -> str:
    def rep(m):
        d = m.group(0)
        if d in FLAGS_NUMBERS:
            cid, fb = FLAGS_NUMBERS[d]
            return f'<tg-emoji emoji-id="{cid}">{fb}</tg-emoji>'
        return d
    return re.sub(r'\d', rep, text)

# -------------------------------------------------------------
# INDIVIDUAL STYLES IMPLEMENTATION
# -------------------------------------------------------------

# 1. 👑 Ultra Professional VIP Mix (Pro Mix)
def style_pro_mix(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    
    vip_badges = [
        TAG_ATTR_CHECK_NEON,
        TAG_DSPSIR_APPLE_GLOW,
        TAG_ATTR_CHECK_GOLD,
        TAG_BLUE_VERIFIED,
        TAG_SHUZI_DIAMOND,
        TAG_ATTR_BUTTON_GREEN,
        TAG_DSPSIR_CROWN,
        TAG_ATTR_CHECK_BLUE,
    ]

    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)

        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))
        
        # Header line (Line 0)
        if i == 0:
            if is_pure_english and len(line_clean) <= 24 and not line_clean.startswith("@"):
                hdr_font = to_abc_font(line_clean)
                escaped = f"{TAG_SHUZI_FIRE} {TAG_DSPSIR_CROWN} {hdr_font} {TAG_ATTR_CHECK_NEON} {TAG_SHUZI_FIRE}"
            else:
                escaped = f"{TAG_SHUZI_FIRE} {TAG_DSPSIR_APPLE_GLOW} <b>{escaped}</b> {TAG_ATTR_CHECK_NEON} {TAG_SHUZI_FIRE}"
            decorated.append(escaped)
            continue

        # Submitting/Links lines
        if line_clean.startswith("@") or "submit" in line_clean.lower() or "file" in line_clean.lower() or "link" in line_clean.lower():
            escaped = f"<blockquote>{TAG_HASIB_DOWN} <b>{escaped}</b></blockquote>"
            decorated.append(escaped)
            continue

        # Convert numbers and keywords
        escaped = convert_digits_to_abc(escaped)

        def rep_keyword(m):
            w = m.group(0)
            if len(w) <= 8 and w.isupper() and w not in ["TK", "PM", "AM"]:
                return to_led_screen(w)
            return w
        escaped = re.sub(r'\b[A-Z]{3,8}\b', rep_keyword, escaped)

        badge = vip_badges[(i - 1) % len(vip_badges)]
        escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)

    return "\n".join(decorated)

# 2. ⚡️ Cyber Electric Mix
def style_cyber_mix(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    cyber_badges = [TAG_ELEC_SHOCK1, TAG_ELEC_SHOCK2, TAG_ELEC_SHOCK3, TAG_ATTR_CHECK_NEON, TAG_TARA_LIGHTNING]

    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))

        if i == 0:
            if is_pure_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
                cyber_hdr = to_retro_font(line_clean)
                escaped = f"{TAG_ELEC_SHOCK1} {cyber_hdr} {TAG_ELEC_SHOCK2}"
            else:
                escaped = f"{TAG_ELEC_SHOCK1} ⚡️ <b>{escaped}</b> ⚡️ {TAG_ELEC_SHOCK2}"
            decorated.append(escaped)
            continue

        escaped = convert_digits_to_led(escaped)
        badge = cyber_badges[(i - 1) % len(cyber_badges)]
        escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 3. 🌟 Neon Glow Mix
def style_neon_glow(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    neon_badges = [TAG_ORDER_STAR, TAG_ATTR_STAR, TAG_HASIB_GOLD, TAG_XTREMIST_STAR, TAG_SHUZI_STAR]

    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))

        if i == 0:
            if is_pure_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
                neon_hdr = to_led_screen(line_clean)
                escaped = f"{TAG_ORDER_STAR} {neon_hdr} {TAG_ORDER_STAR}"
            else:
                escaped = f"{TAG_ORDER_STAR} 🌟 <b>{escaped}</b> 🌟 {TAG_ORDER_STAR}"
            decorated.append(escaped)
            continue

        escaped = convert_digits_to_led(escaped)
        badge = neon_badges[(i - 1) % len(neon_badges)]
        escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 4. 💎 3D ABC Font Style
def style_abc(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))

        if is_pure_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            abc_txt = to_abc_font(line_clean)
            if i == 0:
                escaped = f"{TAG_DSPSIR_DIAMOND} {abc_txt} {TAG_DSPSIR_CROWN}"
            else:
                escaped = f"<blockquote>{TAG_ATTR_CHECK_BLUE} {abc_txt}</blockquote>"
        else:
            escaped = convert_digits_to_abc(escaped)
            if i == 0 and len(lines) > 1:
                escaped = f"{TAG_DSPSIR_DIAMOND} <b>{escaped}</b> {TAG_DSPSIR_CROWN}"
            else:
                escaped = f"<blockquote>{TAG_ATTR_CHECK_BLUE} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 5. 🟢 Slime Font Style
def style_slime(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))

        if is_pure_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            slime_txt = to_slime_font(line_clean)
            if i == 0:
                escaped = f"{TAG_ATTR_CIRCLE_GREEN} {slime_txt} {TAG_ATTR_CHECK_GREEN}"
            else:
                escaped = f"<blockquote>{TAG_ATTR_CHECK_GREEN} {slime_txt}</blockquote>"
        else:
            escaped = convert_digits_to_slime(escaped)
            if i == 0 and len(lines) > 1:
                escaped = f"{TAG_ATTR_CIRCLE_GREEN} <b>{escaped}</b> {TAG_ATTR_CHECK_GREEN}"
            else:
                escaped = f"<blockquote>{TAG_ATTR_CHECK_GREEN} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 6. 💀 Bony Skeleton Font Style
def style_bony(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))

        if is_pure_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            bony_txt = to_bony_font(line_clean)
            if i == 0:
                escaped = f"{TAG_SHUZI_FIRE} {bony_txt} {TAG_SHUZI_FIRE}"
            else:
                escaped = f"<blockquote>💀 {bony_txt}</blockquote>"
        else:
            escaped = convert_digits_to_bony(escaped)
            if i == 0 and len(lines) > 1:
                escaped = f"{TAG_SHUZI_FIRE} <b>{escaped}</b> {TAG_SHUZI_FIRE}"
            else:
                escaped = f"<blockquote>💀 {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 7. 🎃 Spooky Letters Style
def style_spooky(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))

        if is_pure_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            spooky_txt = to_spooky_font(line_clean)
            if i == 0:
                escaped = f"🎃 {spooky_txt} 🎃"
            else:
                escaped = f"<blockquote>🎃 {spooky_txt}</blockquote>"
        else:
            if i == 0 and len(lines) > 1:
                escaped = f"🎃 <b>{escaped}</b> 🎃"
            else:
                escaped = f"<blockquote>🎃 {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 8. 🚩 Festive Flags Style
def style_flags(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))

        if is_pure_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            flags_txt = to_flags_font(line_clean)
            if i == 0:
                escaped = f"🚩 {flags_txt} 🚩"
            else:
                escaped = f"<blockquote>🚩 {flags_txt}</blockquote>"
        else:
            escaped = convert_digits_to_flags(escaped)
            if i == 0 and len(lines) > 1:
                escaped = f"🚩 <b>{escaped}</b> 🚩"
            else:
                escaped = f"<blockquote>🚩 {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 9. 🪵 Table Font Style
def style_table(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        is_pure_english = bool(re.search(r'^[A-Za-z0-9\s:_\-+*#@.]+$', line_clean))

        if is_pure_english and len(line_clean) <= 25 and not line_clean.startswith("@"):
            tbl_txt = to_table_font(line_clean)
            if i == 0:
                escaped = f"🪵 {tbl_txt} 🪵"
            else:
                escaped = f"<blockquote>🪵 {tbl_txt}</blockquote>"
        else:
            if i == 0 and len(lines) > 1:
                escaped = f"🪵 <b>{escaped}</b> 🪵"
            else:
                escaped = f"<blockquote>🪵 {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 10. ✨ Attractive VIP Pack Style
def style_attractive(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    badges = [TAG_ATTR_CHECK_NEON, TAG_ATTR_CHECK_GOLD, TAG_ATTR_BUTTON_BLUE, TAG_ATTR_CIRCLE_GREEN, TAG_ATTR_BUTTON_GOLD]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_ATTR_CHECK_NEON} {TAG_ATTR_STAR} <b>{escaped}</b> {TAG_ATTR_CHECK_GOLD}"
        else:
            badge = badges[i % len(badges)]
            escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 11. 🍏 DSPSIR Luxury Pack Style
def style_dspsir(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    badges = [TAG_DSPSIR_APPLE_GLOW, TAG_DSPSIR_CROWN, TAG_DSPSIR_DIAMOND, TAG_DSPSIR_CHECK_BLUE, TAG_DSPSIR_MEDAL]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_DSPSIR_APPLE_GLOW} {TAG_DSPSIR_CROWN} <b>{escaped}</b> {TAG_DSPSIR_DIAMOND}"
        else:
            badge = badges[i % len(badges)]
            escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 12. ⚡️ Electric Shock Style
def style_electric(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    shocks = [TAG_ELEC_SHOCK1, TAG_ELEC_SHOCK2, TAG_ELEC_SHOCK3, TAG_ELEC_SHOCK4, TAG_ELEC_SHOCK5]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_ELEC_SHOCK1} ⚡️ <b>{escaped}</b> ⚡️ {TAG_ELEC_SHOCK2}"
        else:
            shk = shocks[i % len(shocks)]
            escaped = f"<blockquote>{shk} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 13. LED Screen Style
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
            if i == 0 and len(lines) > 1:
                escaped = f"{TAG_HASIB_FIRE} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_HASIB_FIRE}"
            else:
                badges = [TAG_BLUE_VERIFIED, TAG_GREEN_VERIFIED, TAG_RED_VERIFIED, TAG_HASIB_SHIELD, TAG_HASIB_GOLD]
                badge = badges[i % len(badges)]
                escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 14. Retro Font Style
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
            if i == 0 and len(lines) > 1:
                escaped = f"{TAG_CROWN} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_DIAMOND}"
            else:
                badges = [TAG_RED_VERIFIED, TAG_BLUE_VERIFIED, TAG_XTREMIST_BLUE, TAG_HASIB_GOLD]
                badge = badges[i % len(badges)]
                escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 15. Cat Font Style
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
            if i == 0:
                escaped = f"{TAG_HEART} {TAG_SPARKLES} <b>{escaped}</b> {TAG_ROSE} {TAG_HEART}"
            else:
                escaped = f"<blockquote>{TAG_HEART} {escaped} {TAG_BLUE_VERIFIED}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 16. Hasib Pack Style
def style_hasib(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    badges = [TAG_RED_VERIFIED, TAG_HASIB_SHIELD, TAG_HASIB_GOLD, TAG_HASIB_FIRE, TAG_HASIB_HUNDRED]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_HASIB_FIRE} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_HASIB_GOLD} {TAG_HASIB_FIRE}"
        else:
            badge = badges[i % len(badges)]
            escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 17. XtremistQFS Style
def style_xtremist(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    badges = [TAG_XTREMIST_BLUE, TAG_XTREMIST_CHECK, TAG_XTREMIST_GLOW, TAG_XTREMIST_STAR]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_XTREMIST_STAR} {TAG_XTREMIST_BLUE} <b>{escaped}</b> {TAG_XTREMIST_GLOW}"
        else:
            badge = badges[i % len(badges)]
            escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 18. Tara Lightning Style
def style_tara(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    lightnings = [TAG_TARA_LIGHTNING, TAG_TARA_LIGHTNING2, TAG_TARA_LIGHTNING3]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_TARA_LIGHTNING} ⚡️ <b>{escaped}</b> ⚡️ {TAG_TARA_LIGHTNING2}"
        else:
            lt = lightnings[i % len(lightnings)]
            escaped = f"<blockquote>{lt} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 19. OrderEmoji Star Style
def style_order(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    stars = [TAG_ORDER_STAR, TAG_ORDER_STAR2, TAG_ORDER_STAR]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_ORDER_STAR} 🌟 <b>{escaped}</b> 🌟 {TAG_ORDER_STAR2}"
        else:
            st = stars[i % len(stars)]
            escaped = f"<blockquote>{st} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 20. Blockquotes Frame Style
def style_quotes(text: str) -> str:
    lines = text.strip().splitlines()
    decorated = []
    badges = [TAG_BLUE_VERIFIED, TAG_GREEN_VERIFIED, TAG_RED_VERIFIED, TAG_HASIB_SHIELD]
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean:
            decorated.append("")
            continue
        escaped = html.escape(line_clean)
        escaped = convert_existing_emojis_to_premium(escaped)
        if i == 0 and len(lines) > 1:
            escaped = f"{TAG_HASIB_FIRE} {TAG_RED_VERIFIED} <b>{escaped}</b> {TAG_BLUE_VERIFIED} {TAG_HASIB_FIRE}"
        else:
            badge = badges[i % len(badges)]
            escaped = f"<blockquote>{badge} {escaped}</blockquote>"
        decorated.append(escaped)
    return "\n".join(decorated)

# 21. Smart All-in-One Style
def style_smart(text: str) -> str:
    return style_pro_mix(text)

# -------------------------------------------------------------
# MAIN DISPATCHER
# -------------------------------------------------------------

def decorate_text(text: str, style: str = "pro_mix") -> str:
    """Main decoration entry point."""
    style = style.lower().strip()
    
    style_map = {
        "pro_mix": style_pro_mix,
        "cyber_mix": style_cyber_mix,
        "neon_glow": style_neon_glow,
        "abc": style_abc,
        "slime": style_slime,
        "bony": style_bony,
        "spooky": style_spooky,
        "flags": style_flags,
        "table": style_table,
        "attractive": style_attractive,
        "dspsir": style_dspsir,
        "electric": style_electric,
        "led": style_led,
        "retro": style_retro,
        "cat": style_cat,
        "hasib": style_hasib,
        "xtremist": style_xtremist,
        "tara": style_tara,
        "order": style_order,
        "quotes": style_quotes,
        "smart": style_smart,
    }
    
    fn = style_map.get(style, style_pro_mix)
    return fn(text)

def get_plain_text_for_copy(text: str, style: str = "pro_mix") -> str:
    """Returns a clean plain text version with standard emojis for CopyTextButton."""
    decorated = decorate_text(text, style=style)
    # Strip HTML tags
    clean = re.sub(r'<tg-emoji[^>]*>(.*?)</tg-emoji>', r'\1', decorated)
    clean = re.sub(r'</?blockquote>', '', clean)
    clean = re.sub(r'</?[bi]>', '', clean)
    return html.unescape(clean)

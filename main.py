import logging
import re
import html
import os
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any, List
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
    CopyTextButton,
)
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    ContextTypes,
    filters,
)

from config import BOT_TOKEN, DEFAULT_STYLE
from database import (
    init_db,
    get_user_settings,
    update_user_style,
    add_custom_pack,
    get_user_custom_packs,
    add_custom_emoji,
    log_format_stat,
)
from emoji_engine import (
    decorate_text,
    get_plain_text_for_copy,
    TAG_BLUE_VERIFIED,
    TAG_RED_VERIFIED,
    TAG_GREEN_VERIFIED,
    TAG_XTREMIST_BLUE,
    TAG_HASIB_GOLD,
    TAG_HASIB_SHIELD,
    TAG_HASIB_FIRE,
    TAG_HASIB_DOWN,
    TAG_TARA_LIGHTNING,
    TAG_ORDER_STAR,
    TAG_ATTR_CHECK_NEON,
    TAG_ATTR_CHECK_GOLD,
    TAG_ATTR_BUTTON_BLUE,
    TAG_ATTR_CIRCLE_GREEN,
    TAG_DSPSIR_APPLE_GLOW,
    TAG_DSPSIR_CROWN,
    TAG_DSPSIR_DIAMOND,
    TAG_ELEC_SHOCK1,
    TAG_ELEC_SHOCK2,
    TAG_SHUZI_FIRE,
    TAG_SHUZI_DIAMOND,
    TAG_CROWN,
    TAG_DIAMOND,
    TAG_HEART,
    TAG_SPARKLES,
    TAG_HAND_WAVE,
    TAG_POINT_DOWN,
)

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# In-memory store for last input per user (to allow instant style toggling)
user_last_text: Dict[int, str] = {}

STYLE_NAMES = {
    "pro_mix": f"{TAG_DSPSIR_CROWN} আল্ট্রা প্রফেশনাল ভিআইপি মিক্স",
    "cyber_mix": f"{TAG_ELEC_SHOCK1} সাইবার ইলেকট্রিক মিক্স",
    "neon_glow": f"{TAG_ORDER_STAR} নিয়ন গ্লো মিক্স",
    "smart": f"{TAG_BLUE_VERIFIED} স্মার্ট অল-ইন-ওয়ান",
    "abc": f"{TAG_DSPSIR_DIAMOND} ৩ডি এবিসি ফন্ট (ABCEmoji)",
    "slime": f"{TAG_ATTR_CIRCLE_GREEN} স্লিম ফন্ট (SlimeFont)",
    "retro": f"{TAG_TARA_LIGHTNING} রেট্রো ফন্ট (RetroFont)",
    "led": f"{TAG_ORDER_STAR} এলইডি স্ক্রিন (LedScreen)",
    "bony": f"{TAG_SHUZI_FIRE} বোনি স্কেলেটন ফন্ট (BonyFont)",
    "spooky": f"🎃 স্পুকি গোস্ট ফন্ট (SpookyLetters)",
    "flags": f"🚩 ফেস্টিভ ফ্ল্যাগ ফন্ট (FestiveFlags)",
    "table": f"🪵 টেবিল উডেন ফন্ট (TableFont)",
    "attractive": f"{TAG_ATTR_CHECK_NEON} অ্যাট্রাক্টিভ ভিআইপি (@OrderEmoji)",
    "dspsir": f"{TAG_DSPSIR_APPLE_GLOW} ডিএসপি অ্যাপল ও লাক্সারি",
    "electric": f"{TAG_ELEC_SHOCK2} ইলেকট্রিক শক (@FreeStecker)",
    "hasib": f"{TAG_RED_VERIFIED} হাসিব ভেরিফাইড (Emoji_hasib)",
    "xtremist": f"{TAG_XTREMIST_BLUE} এক্সট্রিমিস্ট (@XtremistQFS)",
    "tara": f"{TAG_TARA_LIGHTNING} তারা লাইটনিং (@stickerXtara)",
    "order": f"{TAG_ORDER_STAR} অর্ডার স্টার (@OrderEmoji)",
    "cat": f"{TAG_HEART} ক্যাট ফন্ট (CatFontEmoji)",
    "quotes": f"{TAG_RED_VERIFIED} ব্লককোট ফ্রেম",
}

def get_style_keyboard(current_style: str = "pro_mix", text_to_copy: str = "") -> InlineKeyboardMarkup:
    """Builds inline keyboard with 20+ styles organized logically + Native 1-Click Copy button."""
    buttons = []

    # TOP ROW: Real 1-Click Copy Button using Telegram's native CopyTextButton
    if text_to_copy:
        buttons.append([
            InlineKeyboardButton(
                text="📋 এক ক্লিকে সম্পূর্ণ কপি করুন",
                copy_text=CopyTextButton(text=text_to_copy),
                icon_custom_emoji_id="5411309092427834175" # Blue Verified
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text="📋 এক ক্লিকে কপি করার উপায়",
                callback_data="copy_guide",
                icon_custom_emoji_id="5411309092427834175"
            )
        ])

    # Category 1: 🌟 সুপার প্রফেশনাল ও মিক্স স্টাইল (Most popular)
    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'pro_mix' else ''}👑 প্রফেশনাল ভিআইপি",
            callback_data="style_pro_mix",
            icon_custom_emoji_id="6269556155031228243" # Crown
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'cyber_mix' else ''}⚡️ সাইবার ইলেকট্রিক",
            callback_data="style_cyber_mix",
            icon_custom_emoji_id="6323076240722891410" # Electric shock
        ),
    ])

    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'neon_glow' else ''}🌟 নিয়ন গ্লো মিক্স",
            callback_data="style_neon_glow",
            icon_custom_emoji_id="5355033944129552118" # Order Star
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'smart' else ''}✨ স্মার্ট অল-ইন-ওয়ান",
            callback_data="style_smart",
            icon_custom_emoji_id="5411309092427834175" # Blue Verified
        ),
    ])

    # Category 2: 🔠 থ্রি-ডি ও নিয়ন ফন্ট প্যাকসমূহ
    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'abc' else ''}💎 ৩ডি এবিসি ফন্ট",
            callback_data="style_abc",
            icon_custom_emoji_id="5226734466315067436" # ABC Letter A
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'slime' else ''}🟢 স্লিম ফন্ট",
            callback_data="style_slime",
            icon_custom_emoji_id="5206212670193152371" # Slime Letter A
        ),
    ])

    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'led' else ''}🟢 এলইডি স্ক্রিন",
            callback_data="style_led",
            icon_custom_emoji_id="5357372145800334358" # LED Letter A
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'retro' else ''}🕹 রেট্রো ফন্ট",
            callback_data="style_retro",
            icon_custom_emoji_id="5386505875336744038" # Retro Letter A
        ),
    ])

    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'bony' else ''}💀 বোনি স্কেলেটন",
            callback_data="style_bony",
            icon_custom_emoji_id="5447127715222138904" # Bony Letter A
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'spooky' else ''}🎃 স্পুকি গোস্ট",
            callback_data="style_spooky",
            icon_custom_emoji_id="5334564018327665783" # Spooky Letter A
        ),
    ])

    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'flags' else ''}🚩 ফেস্টিভ ফ্ল্যাগ",
            callback_data="style_flags",
            icon_custom_emoji_id="5425026290258292141" # Flags Letter A
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'table' else ''}🪵 টেবিল উডেন",
            callback_data="style_table",
            icon_custom_emoji_id="5210820276748566172" # Table Letter A
        ),
    ])

    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'cat' else ''}🐱 ক্যাট ফন্ট",
            callback_data="style_cat",
            icon_custom_emoji_id="5438357284629535015" # Cat Letter A
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'quotes' else ''}💬 ব্লককোট ফ্রেম",
            callback_data="style_quotes",
            icon_custom_emoji_id="5843855334707302293" # Shield
        ),
    ])

    # Category 3: 👑 স্পেশাল ভেরিফাইড ও আইকন প্যাকসমূহ
    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'attractive' else ''}✨ অ্যাট্রাক্টিভ ভিআইপি",
            callback_data="style_attractive",
            icon_custom_emoji_id="5211112665237175703" # Attractive Neon Check
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'dspsir' else ''}🍏 অ্যাপল লাক্সারি",
            callback_data="style_dspsir",
            icon_custom_emoji_id="6273556792513402505" # Apple Glow
        ),
    ])

    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'electric' else ''}⚡️ ইলেকট্রিক শক",
            callback_data="style_electric",
            icon_custom_emoji_id="6323138152676464326" # Electric Shock
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'hasib' else ''}🔴 হাসিব ভেরিফাইড",
            callback_data="style_hasib",
            icon_custom_emoji_id="5992524725715209996" # Red Verified
        ),
    ])

    buttons.append([
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'xtremist' else ''}🔵 এক্সট্রিমিস্ট",
            callback_data="style_xtremist",
            icon_custom_emoji_id="6267313108360895894" # Xtremist Blue
        ),
        InlineKeyboardButton(
            text=f"{'✓ ' if current_style == 'tara' else ''}⚡️ তারা লাইটনিং",
            callback_data="style_tara",
            icon_custom_emoji_id="6271656548657795731" # Tara Lightning
        ),
    ])

    return InlineKeyboardMarkup(buttons)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    user = update.effective_user
    settings = get_user_settings(user.id, user.username or "", user.first_name or "")
    current_style = settings.get("style", "pro_mix")
    
    welcome_text = (
        f"{TAG_HAND_WAVE} <b>আসসালামু আলাইকুম, {html.escape(user.first_name or 'বন্ধু')}!</b>\n\n"
        f"{TAG_DSPSIR_CROWN} {TAG_BLUE_VERIFIED} <b>টেলিগ্রাম প্রিমিয়াম অটো-ইমোজি বটে আপনাকে স্বাগতম!</b>\n\n"
        f"এই বটে আপনি যেকোনো ইংরেজি বা বাংলা টেক্সট, পোস্ট, দামের তালিকা বা রিপোর্ট পাঠালেই বট স্বয়ংক্রিয়ভাবে "
        f"<b>টেলিগ্রাম প্রিমিয়াম কাস্টম ইমোজি ও ফ্রেম</b> দিয়ে আকর্ষণীয়ভাবে সাজিয়ে দেবে।\n\n"
        f"{TAG_SPARKLES} <b>বর্তমানে সক্রিয় স্টাইল:</b> {STYLE_NAMES.get(current_style, current_style)}\n\n"
        f"👇 <b>কীভাবে ব্যবহার করবেন:</b>\n"
        f"১. যেকোনো সাধারণ টেক্সট বা পোস্ট লিখে সরাসরি এই বটে সেন্ড করুন।\n"
        f"২. বট প্রিমিয়াম ইমোজি দিয়ে সাজিয়ে <b>📋 এক ক্লিকে সম্পূর্ণ কপি</b> বাটন সহ মেসেজ দেবে।\n"
        f"৩. নিচের বাটনগুলো চেপে এক ক্লিকে যেকোনো স্টাইলে রূপান্তর করতে পারবেন।\n"
        f"৪. যেকোনো চ্যাটে <code>@textaddemojibot আপনার লেখা</code> লিখেও সরাসরি প্রিমিয়াম ইমোজি সহ পাঠাতে পারবেন!\n\n"
        f"💡 নতুন কোনো প্রিমিয়াম ইমোজি প্যাকের লিংক সেন্ড করলেও বট তা যুক্ত করে নেবে।"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_style_keyboard(current_style)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        f"{TAG_CROWN} {TAG_BLUE_VERIFIED} <b>টেলিগ্রাম প্রিমিয়াম অটো-ইমোজি বট গাইড:</b>\n\n"
        f"<b>১. টেক্সট পাঠানো:</b>\n"
        f"যে কোনো টেক্সট বা পোস্ট লিখলেই বট স্বয়ংক্রিয়ভাবে প্রফেশনাল ফন্ট ও প্রিমিয়াম ইমোজি দিয়ে সাজিয়ে দেবে।\n\n"
        f"<b>২. এক ক্লিকে কপি:</b>\n"
        f"মেসেজের নিচে থাকা <b>📋 এক ক্লিকে সম্পূর্ণ কপি করুন</b> বাটনে ক্লিক করলেই পুরো ফরম্যাটেড টেক্সট ক্লিপবোর্ডে কপি হয়ে যাবে!\n\n"
        f"<b>৩. স্টাইল পরিবর্তন:</b>\n"
        f"/style কমান্ড দিয়ে বা মেসেজের নিচের বাটনগুলোতে ক্লিক করে মোট ২০+ প্রিমিয়াম স্টাইল থেকে পছন্দমতো বেছে নিতে পারবেন।\n\n"
        f"<b>৪. নতুন ইমোজি প্যাক যোগ:</b>\n"
        f"যেকোনো টেলিগ্রাম কাস্টম ইমোজি প্যাকের লিংক (যেমন: <code>https://t.me/addemoji/pack_name</code>) সেন্ড করলেই বট তা সংরক্ষণ করে নেবে!"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def style_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /style command."""
    user = update.effective_user
    settings = get_user_settings(user.id, user.username or "", user.first_name or "")
    current_style = settings.get("style", "pro_mix")
    
    text = (
        f"{TAG_DSPSIR_CROWN} {TAG_ATTR_CHECK_NEON} <b>আপনার পছন্দের প্রিমিয়াম ইমোজি স্টাইল নির্বাচন করুন:</b>\n\n"
        f"বর্তমান স্টাইল: <b>{STYLE_NAMES.get(current_style, current_style)}</b>\n\n"
        f"নিচের ক্যাটাগরিগুলো থেকে আপনার পছন্দের স্টাইল বেছে নিন:"
    )
    await update.message.reply_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_style_keyboard(current_style)
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button clicks."""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data
    
    if data == "copy_guide":
        await query.answer(
            text="📋 কপি করার টিপস:\nমেসেজের নিচে থাকা 'এক ক্লিকে সম্পূর্ণ কপি করুন' বাটনে চাপ দিন অথবা মেসেজের ওপর চেপে ধরে 'Copy Text' চাপুন!",
            show_alert=True
        )
        return
        
    if data.startswith("style_"):
        new_style = data.replace("style_", "")
        update_user_style(user_id, new_style)
        
        if user_id in user_last_text:
            raw_text = user_last_text[user_id]
            formatted_text = decorate_text(raw_text, style=new_style)
            copy_text_payload = get_plain_text_for_copy(raw_text, style=new_style)
            try:
                await query.edit_message_text(
                    text=formatted_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_style_keyboard(new_style, text_to_copy=copy_text_payload)
                )
            except Exception as e:
                logger.error(f"Error editing message: {e}")
                try:
                    await query.edit_message_reply_markup(reply_markup=get_style_keyboard(new_style, text_to_copy=copy_text_payload))
                except Exception:
                    pass
        else:
            await query.edit_message_reply_markup(reply_markup=get_style_keyboard(new_style))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages from users."""
    user = update.effective_user
    text = update.message.text
    
    if not text:
        return
        
    # Check if text is a Telegram sticker/emoji pack link
    pack_match = re.search(r"(?:t\.me|telegram\.me)/(?:addemoji|addstickers)/([a-zA-Z0-9_]+)", text)
    if pack_match:
        pack_name = pack_match.group(1)
        try:
            sticker_set = await context.bot.get_sticker_set(pack_name)
            if sticker_set.sticker_type == "custom_emoji":
                emojis_data = [
                    {"emoji": s.emoji, "custom_emoji_id": s.custom_emoji_id}
                    for s in sticker_set.stickers if s.custom_emoji_id
                ]
                add_custom_pack(user.id, pack_name, sticker_set.title, emojis_data)
                success_msg = (
                    f"{TAG_SHUZI_FIRE} {TAG_ATTR_CHECK_NEON} <b>প্রিমিয়াম ইমোজি প্যাক যুক্ত হয়েছে!</b>\n\n"
                    f"{TAG_DSPSIR_DIAMOND} <b>নাম:</b> {html.escape(sticker_set.title)}\n"
                    f"{TAG_BLUE_VERIFIED} <b>ইমোজি সংখ্যা:</b> {len(emojis_data)} টি\n\n"
                    f"এখন এই প্যাকের ইমোজিগুলোও আপনার অ্যাকাউন্টে ব্যবহারের জন্য প্রস্তুত! {TAG_SPARKLES}"
                )
                await update.message.reply_text(success_msg, parse_mode=ParseMode.HTML)
                return
            else:
                await update.message.reply_text(
                    f"{TAG_RED_VERIFIED} এটি সাধারণ স্টিকার প্যাক। অনুগ্রহ করে টেলিগ্রাম প্রিমিয়াম <b>কাস্টম ইমোজি প্যাক</b> এর লিংক দিন।",
                    parse_mode=ParseMode.HTML
                )
                return
        except Exception as e:
            logger.error(f"Error fetching sticker pack: {e}")
            await update.message.reply_text(f"❌ প্যাকটি আনতে সমস্যা হয়েছে: {e}")
            return

    # Check if message contains custom emojis sent directly
    if update.message.entities:
        new_emojis_count = 0
        for ent in update.message.entities:
            if ent.type == "custom_emoji" and ent.custom_emoji_id:
                char = text[ent.offset : ent.offset + ent.length]
                add_custom_emoji(user.id, char, ent.custom_emoji_id)
                new_emojis_count += 1
        if new_emojis_count > 0:
            logger.info(f"Learned {new_emojis_count} custom emojis from user {user.id}")

    # Save to user last text for quick style swapping
    user_last_text[user.id] = text

    # Retrieve user's preferred style (defaults to pro_mix)
    settings = get_user_settings(user.id, user.username or "", user.first_name or "")
    active_style = settings.get("style", "pro_mix")
    
    # Decorate text
    formatted_text = decorate_text(text, style=active_style)
    copy_text_payload = get_plain_text_for_copy(text, style=active_style)
    log_format_stat(user.id, len(text), active_style)
    
    try:
        await update.message.reply_text(
            formatted_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_style_keyboard(active_style, text_to_copy=copy_text_payload)
        )
    except Exception as e:
        logger.error(f"Error formatting message with HTML: {e}")
        # Safe fallback
        await update.message.reply_text(
            f"{TAG_BLUE_VERIFIED} {text}",
            parse_mode=ParseMode.HTML,
            reply_markup=get_style_keyboard(active_style, text_to_copy=text)
        )

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline queries (@textaddemojibot query)."""
    query = update.inline_query.query.strip()
    if not query:
        return

    results = []
    top_styles = [
        ("pro_mix", "👑 আল্ট্রা প্রফেশনাল ভিআইপি মিক্স"),
        ("cyber_mix", "⚡️ সাইবার ইলেকট্রিক মিক্স"),
        ("abc", "💎 ৩ডি এবিসি ফন্ট (ABCEmoji)"),
        ("slime", "🟢 স্লিম ফন্ট (SlimeFont)"),
        ("neon_glow", "🌟 নিয়ন গ্লো মিক্স"),
        ("led", "🟢 এলইডি স্ক্রিন (LedScreen)"),
        ("retro", "🕹 রেট্রো ফন্ট (RetroFont)"),
        ("attractive", "✨ অ্যাট্রাক্টিভ ভিআইপি ভেরিফাইড"),
        ("dspsir", "🍏 অ্যাপল লাক্সারি প্যাক"),
        ("bony", "💀 বোনি স্কেলেটন ফন্ট"),
    ]

    for style_key, title in top_styles:
        decorated = decorate_text(query, style=style_key)
        results.append(
            InlineQueryResultArticle(
                id=f"res_{style_key}",
                title=title,
                description=query[:60],
                input_message_content=InputTextMessageContent(
                    message_text=decorated,
                    parse_mode=ParseMode.HTML
                )
            )
        )

    await update.inline_query.answer(results, cache_time=1)

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Simple HTTP server to support 24/7 cloud hosting on Render/Koyeb Free Web Services."""
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Telegram Premium Emoji Bot is online and healthy!")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress routine GET logging to keep console clean
        return

def start_health_check_server():
    port = int(os.environ.get("PORT", 8080))
    try:
        server = ThreadingHTTPServer(("0.0.0.0", port), HealthCheckHandler)
        logger.info(f"Health check HTTP server running on port {port}")
        server.serve_forever()
    except Exception as e:
        logger.warning(f"Could not bind HTTP server to port {port}: {e}")

def main():
    """Start the bot."""
    init_db()
    
    # Start Health Check HTTP server for 24/7 Cloud Web Service deployment (Render / Koyeb)
    health_thread = threading.Thread(target=start_health_check_server, daemon=True)
    health_thread.start()

    logger.info("Initializing Telegram Premium Emoji Bot with 20+ Dedicated Styles, New Packs & 1-Click Copy...")
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("style", style_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.add_handler(InlineQueryHandler(handle_inline_query))
    
    logger.info("Bot is polling for updates...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

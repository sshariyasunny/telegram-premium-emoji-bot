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

from config import BOT_TOKEN
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
    "led": f"{TAG_ORDER_STAR} এলইডি স্ক্রিন (LedScreenEmoji)",
    "retro": f"{TAG_TARA_LIGHTNING} রেট্রো ফন্ট (RetroFontEmoji)",
    "hasib": f"{TAG_RED_VERIFIED} হাসিব ভেরিফাইড (Emoji_hasib)",
    "xtremist": f"{TAG_XTREMIST_BLUE} এক্সট্রিমিস্ট (@XtremistQFS)",
    "tara": f"{TAG_TARA_LIGHTNING} তারা লাইটনিং (@stickerXtara)",
    "order": f"{TAG_ORDER_STAR} অর্ডার স্টার (@OrderEmoji)",
    "cat": f"{TAG_HEART} ক্যাট ফন্ট (CatFontEmoji)",
    "quotes": f"{TAG_RED_VERIFIED} ব্লককোট ফ্রেম",
    "smart": f"{TAG_BLUE_VERIFIED} স্মার্ট অল-ইন-ওয়ান",
}

def get_style_keyboard(current_style: str = "led", text_to_copy: str = "") -> InlineKeyboardMarkup:
    """Builds inline keyboard with ALL user favorite styles + Native 1-Click Copy button."""
    buttons = [
        # Row 1: User's Top Font Packs
        [
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
        ],
        # Row 2: Hasib & Xtremist Verified
        [
            InlineKeyboardButton(
                text=f"{'✓ ' if current_style == 'hasib' else ''}🔴 হাসিব প্যাক",
                callback_data="style_hasib",
                icon_custom_emoji_id="5992524725715209996" # Red Verified
            ),
            InlineKeyboardButton(
                text=f"{'✓ ' if current_style == 'xtremist' else ''}🔵 এক্সট্রিমিস্ট",
                callback_data="style_xtremist",
                icon_custom_emoji_id="6267313108360895894" # Xtremist Blue Verified
            ),
        ],
        # Row 3: Tara Lightning & Order Star
        [
            InlineKeyboardButton(
                text=f"{'✓ ' if current_style == 'tara' else ''}⚡️ তারা লাইটনিং",
                callback_data="style_tara",
                icon_custom_emoji_id="6271656548657795731" # Tara Lightning
            ),
            InlineKeyboardButton(
                text=f"{'✓ ' if current_style == 'order' else ''}🌟 অর্ডার প্যাক",
                callback_data="style_order",
                icon_custom_emoji_id="5355033944129552118" # Order Star
            ),
        ],
        # Row 4: Cat Font & Blockquotes
        [
            InlineKeyboardButton(
                text=f"{'✓ ' if current_style == 'cat' else ''}🐱 ক্যাট ফন্ট",
                callback_data="style_cat",
                icon_custom_emoji_id="5438357284629535015" # Cat Letter A
            ),
            InlineKeyboardButton(
                text=f"{'✓ ' if current_style == 'quotes' else ''}💬 ব্লককোট ফ্রেম",
                callback_data="style_quotes",
                icon_custom_emoji_id="5843855334707302293" # Shield Badge
            ),
        ],
        # Row 5: Smart Mix
        [
            InlineKeyboardButton(
                text=f"{'✓ ' if current_style == 'smart' else ''}✨ স্মার্ট অল-ইন-ওয়ান",
                callback_data="style_smart",
                icon_custom_emoji_id="5411309092427834175" # Blue Verified
            ),
        ],
    ]
    
    # Row 6: Real 1-Click Copy Button using Telegram's native CopyTextButton
    if text_to_copy:
        buttons.append([
            InlineKeyboardButton(
                text="📋 এক ক্লিকে সরাসরি কপি করুন",
                copy_text=CopyTextButton(text=text_to_copy),
                icon_custom_emoji_id="5411309092427834175" # Blue Verified
            )
        ])
    else:
        buttons.append([
            InlineKeyboardButton(
                text="📋 কপি করার উপায়",
                callback_data="copy_guide",
                icon_custom_emoji_id="5411309092427834175" # Blue Verified
            )
        ])
        
    return InlineKeyboardMarkup(buttons)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command with user's favorite custom emoji packs."""
    user = update.effective_user
    settings = get_user_settings(user.id, user.username or "", user.first_name or "")
    current_style = settings.get("style", "led")
    
    welcome_text = (
        f"{TAG_HAND_WAVE} <b>আসসালামু আলাইকুম, {html.escape(user.first_name or 'বন্ধু')}!</b> {TAG_BLUE_VERIFIED}\n\n"
        f"{TAG_HASIB_FIRE} {TAG_RED_VERIFIED} <b>আপনার পছন্দের প্রিমিয়াম ইমোজি বটে স্বাগতম!</b> {TAG_BLUE_VERIFIED} {TAG_HASIB_FIRE}\n\n"
        f"আপনার পছন্দের সবকটি প্যাক আলাদা আলাদা স্টাইল হিসেবে যুক্ত করা হয়েছে:\n"
        f"• <b>LedScreenEmoji:</b> এলইডি স্ক্রিন সবুজ বর্ণমালা (A-Z) ও এলইডি সংখ্যা\n"
        f"• <b>RetroFontEmoji:</b> ৩ডি রেট্রো ফন্ট বর্ণমালা ও নম্বর\n"
        f"• <b>CatFontEmoji:</b> কিউট ক্যাট ফন্ট বর্ণমালা ও সংখ্যা\n"
        f"• <b>Emoji_hasib:</b> রেড ভেরিফাইড {TAG_RED_VERIFIED}, শিল্ড {TAG_HASIB_SHIELD}, গোল্ড মেডেল {TAG_HASIB_GOLD}, ফায়ার {TAG_HASIB_FIRE} ও ডাউন অ্যারো {TAG_HASIB_DOWN}\n"
        f"• <b>XtremistQFS:</b> ব্লু ভেরিফাইড {TAG_XTREMIST_BLUE} ও প্রিমিয়াম স্টার\n"
        f"• <b>stickerXtara:</b> অ্যানিমেটেড লাইটনিং {TAG_TARA_LIGHTNING}\n"
        f"• <b>OrderEmoji:</b> গ্লোয়িং অর্ডার স্টার {TAG_ORDER_STAR}\n"
        f"• <b>টেলিগ্রাম ব্লককোট:</b> প্রতিটি পোস্ট সুন্দর ফ্রেমযুক্ত ফর্মে সাজাবে!\n\n"
        f"{TAG_ORDER_STAR} <b>বর্তমানে সক্রিয় স্টাইল:</b> {STYLE_NAMES.get(current_style, current_style)}\n\n"
        f"{TAG_POINT_DOWN} <b>কীভাবে ব্যবহার করবেন:</b>\n"
        f"{TAG_RED_VERIFIED} <b>১.</b> যেকোনো লেখা সরাসরি সেন্ড করুন।\n"
        f"{TAG_BLUE_VERIFIED} <b>২.</b> বট স্বয়ংক্রিয়ভাবে ইমোজি ও ফ্রেম দিয়ে সাজিয়ে দেবে।\n"
        f"{TAG_GREEN_VERIFIED} <b>৩.</b> নিচে <b>'📋 এক ক্লিকে সরাসরি কপি করুন'</b> বাটনে চাপ দিলে সরাসরি কপি হয়ে যাবে!\n"
        f"{TAG_HASIB_SHIELD} <b>৪.</b> নিচের যেকোনো বাটনে চাপ দিয়ে যেকোনো মুহূর্তে অন্য স্টাইলে বদলে নিতে পারবেন!"
    )
    
    await update.message.reply_text(
        welcome_text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_style_keyboard(current_style)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    help_text = (
        f"{TAG_DIAMOND} <b>বট ব্যবহারের পূর্ণাঙ্গ নির্দেশিকা</b> {TAG_BLUE_VERIFIED}\n\n"
        f"{TAG_RED_VERIFIED} <b>১. টেক্সট সাজানো:</b>\n"
        f"যেকোনো পোস্ট, অফার বা প্রাইস লিস্ট পাঠান। বট স্বয়ংক্রিয়ভাবে এলইডি বর্ণমালা, রেট্রো ফন্ট ও ভেরিফাইড ব্যাজ সহকারে ফ্রেম তৈরি করে দেবে।\n\n"
        f"{TAG_BLUE_VERIFIED} <b>২. এক ক্লিকে কপি করার উপায়:</b>\n"
        f"• মেসেজের নিচের <b>'📋 এক ক্লিকে সরাসরি কপি করুন'</b> বাটনে চাপ দিন — সাথে সাথে পুরো লেখা কপি হয়ে যাবে!\n"
        f"• অথবা মোবাইলে মেসেজের ওপর ১ সেকেন্ড চেপে ধরে (Long Press) <b>'Copy Text'</b> চাপলে সমস্ত অ্যানিমেটেড ইমোজি সহ কপি হবে!\n\n"
        f"{TAG_GREEN_VERIFIED} <b>৩. ইনলাইন মোড:</b>\n"
        f"যেকোনো চ্যাটে লিখুন:\n"
        f"<code>@{context.bot.username} আপনার মেসেজ</code>\n"
        f"এরপর যেকোনো স্টাইলে ক্লিক করলেই সরাসরি চলে যাবে! {TAG_HASIB_FIRE}"
    )
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def style_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /style command."""
    user = update.effective_user
    settings = get_user_settings(user.id)
    current_style = settings.get("style", "led")
    
    text = (
        f"{TAG_CROWN} {TAG_BLUE_VERIFIED} <b>আপনার পছন্দের প্রিমিয়াম ইমোজি স্টাইল নির্বাচন করুন:</b>\n\n"
        f"বর্তমান স্টাইল: <b>{STYLE_NAMES.get(current_style, current_style)}</b> {TAG_BLUE_VERIFIED}\n\n"
        f"নিচের ৯টি ভিন্ন ভিন্ন স্টাইল থেকে যেকোনোটি বেছে নিন:"
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
            text="📋 কপি করার টিপস:\nমেসেজের নিচে থাকা 'এক ক্লিকে সরাসরি কপি করুন' বাটনে চাপ দিন অথবা মেসেজের ওপর ১ সেকেন্ড চেপে ধরে (Long Press) 'Copy Text' চাপুন!",
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
                    f"{TAG_HASIB_FIRE} {TAG_BLUE_VERIFIED} <b>প্রিমিয়াম ইমোজি প্যাক যুক্ত হয়েছে!</b>\n\n"
                    f"{TAG_DIAMOND} <b>নাম:</b> {html.escape(sticker_set.title)}\n"
                    f"{TAG_BLUE_VERIFIED} <b>ইমোজি সংখ্যা:</b> {len(emojis_data)} টি\n\n"
                    f"এখন এই প্যাকের ইমোজিগুলোও ব্যবহার করা যাবে! {TAG_SPARKLES}"
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

    # Retrieve user's preferred style (defaults to led)
    settings = get_user_settings(user.id, user.username or "", user.first_name or "")
    active_style = settings.get("style", "led")
    
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
        logger.error(f"Failed to send HTML formatted message: {e}")
        await update.message.reply_text(
            f"⚠️ ইমোজি ফরম্যাটিংয়ে ত্রুটি হয়েছে: {e}\n\nআপনার টেক্সট:\n{text}"
        )

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline queries (e.g., @bot text)."""
    query = update.inline_query.query.strip()
    if not query:
        return

    results = []
    styles = [
        ("led", "🟢 এলইডি স্ক্রিন ফন্ট (LedScreenEmoji)"),
        ("retro", "🕹 রেট্রো ৩ডি ফন্ট (RetroFontEmoji)"),
        ("hasib", "🔴 হাসিব ভেরিফাইড প্যাক (Emoji_hasib)"),
        ("xtremist", "🔵 এক্সট্রিমিস্ট ভেরিফাইড (XtremistQFS)"),
        ("tara", "⚡️ তারা লাইটনিং প্যাক (stickerXtara)"),
        ("order", "🌟 অর্ডার স্টার প্যাক (OrderEmoji)"),
        ("cat", "🐱 ক্যাট ফন্ট (CatFontEmoji)"),
        ("quotes", "💬 ব্লককোট ফ্রেম (Blockquotes)"),
        ("smart", "✨ স্মার্ট অল-ইন-ওয়ান (Smart Mix)"),
    ]

    for style_key, title in styles:
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

    logger.info("Initializing Telegram Premium Emoji Bot with 9 Dedicated Packs and Native 1-Click Copy...")
    
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

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)


# =========================
# SOZLAMALAR
# =========================

DISCORD_LINK = "https://discord.gg/G4EMM8GkH"
TELEGRAM_CHANNEL = "https://t.me/asp_community"
CHANNEL_USERNAME = "@asp_community"
ADMIN_USERNAME = "https://t.me/Solh09"


# =========================
# RENDER HEALTH CHECK
# =========================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot online!")

    def log_message(self, format, *args):
        return


def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Health server started on port {port}")
    server.serve_forever()


# =========================
# KLAVIATURALAR
# =========================

def subscription_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 Telegram kanalga obuna bo‘lish",
                url=TELEGRAM_CHANNEL
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Obunani tekshirish",
                callback_data="check_subscription"
            )
        ]
    ])


def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 Profil", callback_data="profile"),
            InlineKeyboardButton("ℹ️ Yordam", callback_data="help")
        ],
        [
            InlineKeyboardButton("🎮 Discord Server", url=DISCORD_LINK)
        ],
        [
            InlineKeyboardButton("📢 Telegram Kanal", url=TELEGRAM_CHANNEL)
        ],
        [
            InlineKeyboardButton("📜 Qoidalar", callback_data="rules"),
            InlineKeyboardButton("📞 Aloqa", url=ADMIN_USERNAME)
        ]
    ])


# =========================
# OBUNANI TEKSHIRISH
# =========================

async def is_subscribed(bot, user_id):
    try:
        member = await bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in ("member", "administrator", "creator"):
            return True

        if member.status == "restricted":
            return getattr(member, "is_member", False)

        return False

    except Exception as e:
        print(f"Subscription check error: {e}")
        return False


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not await is_subscribed(context.bot, user.id):
        text = (
            "👋 <b>Assalomu alaykum!</b>\n\n"
            "🤖 Botdan foydalanish uchun avval "
            "Telegram kanalimizga obuna bo‘ling.\n\n"
            "📢 Kanalga obuna bo‘lgach, "
            "<b>«✅ Obunani tekshirish»</b> tugmasini bosing."
        )

        await update.message.reply_text(
            text,
            parse_mode="HTML",
            reply_markup=subscription_keyboard()
        )
        return

    text = (
        f"👋 <b>Salom, {user.first_name}!</b>\n\n"
        "🎉 <b>ASP Community botiga xush kelibsiz!</b>\n\n"
        "Quyidagi menyudan kerakli bo‘limni tanlang 👇"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================
# YORDAM
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    if not await is_subscribed(context.bot, user.id):
        await update.message.reply_text(
            "📢 Botdan foydalanish uchun avval "
            "Telegram kanalimizga obuna bo‘ling.",
            reply_markup=subscription_keyboard()
        )
        return

    text = (
        "ℹ️ <b>Yordam</b>\n\n"
        "👤 Profil — profilingiz haqida ma'lumot.\n"
        "🎮 Discord — ASP Community Discord serveri.\n"
        "📢 Telegram — bizning Telegram kanalimiz.\n"
        "📜 Qoidalar — server qoidalari.\n"
        "📞 Aloqa — administrator bilan bog‘lanish."
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard()
    )


# =========================
# TUGMALAR
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    user = query.from_user

    # Obunani tekshirish
    if query.data == "check_subscription":

        if await is_subscribed(context.bot, user.id):

            await query.answer("✅ Obuna tasdiqlandi!")

            text = (
                f"👋 <b>Salom, {user.first_name}!</b>\n\n"
                "🎉 <b>ASP Community botiga xush kelibsiz!</b>\n\n"
                "Quyidagi menyudan kerakli bo‘limni tanlang 👇"
            )

            await query.edit_message_text(
                text,
                parse_mode="HTML",
                reply_markup=main_keyboard()
            )

        else:

            await query.answer(
                "❌ Avval Telegram kanalga obuna bo‘ling!",
                show_alert=True
            )

        return

    # Boshqa tugmalar uchun ham obunani tekshiramiz
    if not await is_subscribed(context.bot, user.id):

        await query.answer(
            "❌ Avval kanalga obuna bo‘ling!",
            show_alert=True
        )

        await query.edit_message_text(
            "📢 <b>Botdan foydalanish uchun avval "
            "Telegram kanalimizga obuna bo‘ling.</b>\n\n"
            "Obuna bo‘lgach, quyidagi tugmani bosing:",
            parse_mode="HTML",
            reply_markup=subscription_keyboard()
        )

        return

    # HOME
    if query.data == "home":

        await query.answer()

        await query.edit_message_text(
            "🏠 <b>Asosiy menyu</b>\n\n"
            "Kerakli bo‘limni tanlang 👇",
            parse_mode="HTML",
            reply_markup=main_keyboard()
        )

    # PROFILE
    elif query.data == "profile":

        await query.answer()

        text = (
            "👤 <b>Profil</b>\n\n"
            f"🆔 ID: <code>{user.id}</code>\n"
            f"👤 Ism: {user.first_name}\n"
        )

        if user.username:
            text += f"🔗 Username: @{user.username}\n"

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Orqaga",
                        callback_data="home"
                    )
                ]
            ])
        )

    # HELP
    elif query.data == "help":

        await query.answer()

        text = (
            "ℹ️ <b>Yordam</b>\n\n"
            "👤 Profil — profilingiz.\n"
            "🎮 Discord — Discord serverimiz.\n"
            "📢 Telegram — Telegram kanalimiz.\n"
            "📜 Qoidalar — community qoidalari.\n"
            "📞 Aloqa — administrator."
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Orqaga",
                        callback_data="home"
                    )
                ]
            ])
        )

    # RULES
    elif query.data == "rules":

        await query.answer()

        text = (
            "📜 <b>ASP Community Qoidalari</b>\n\n"
            "1️⃣ Bir-biringizni hurmat qiling.\n"
            "2️⃣ Spam va flood taqiqlanadi.\n"
            "3️⃣ Reklama faqat ruxsat bilan.\n"
            "4️⃣ Haqorat va toxic xatti-harakatlarga yo‘l qo‘yilmaydi.\n"
            "5️⃣ Administratorlar qaroriga rioya qiling.\n\n"
            "🤝 Hammaga yaxshi muhit yaratamiz!"
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "⬅️ Orqaga",
                        callback_data="home"
                    )
                ]
            ])
        )


# =========================
# MAIN
# =========================

def main():

    token = os.environ.get("BOT_TOKEN")

    if not token:
        print("❌ BOT_TOKEN topilmadi!")
        return

    # Render health server
    threading.Thread(
        target=run_health_server,
        daemon=True
    ).start()

    # Telegram bot
    application = Application.builder().token(token).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("🤖 Bot ishga tushdi!")

    application.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()

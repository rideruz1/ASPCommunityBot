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

# ==========================================
# LINKS
# ==========================================

DISCORD_LINK = "https://discord.gg/2bGWXZ6BK"
TELEGRAM_CHANNEL = "https://t.me/asp_community"
ADMIN_USERNAME = "https://t.me/Solh09"


# ==========================================
# RENDER HEALTH SERVER
# ==========================================

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ASP Community Bot is running!")

    def log_message(self, format, *args):
        return


def start_health_server():
    port = int(os.getenv("PORT", "10000"))

    server = HTTPServer(("0.0.0.0", port), HealthHandler)

    print(f"🌐 Health server started on port {port}")

    server.serve_forever()


# ==========================================
# MAIN MENU
# ==========================================

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👤 Profil",
                callback_data="profile"
            ),
            InlineKeyboardButton(
                "ℹ️ Yordam",
                callback_data="help"
            ),
        ],

        [
            InlineKeyboardButton(
                "🎮 Discord Server",
                url=DISCORD_LINK
            ),
        ],

        [
            InlineKeyboardButton(
                "📢 Telegram Kanal",
                url=TELEGRAM_CHANNEL
            ),
        ],

        [
            InlineKeyboardButton(
                "📜 Qoidalar",
                callback_data="rules"
            ),
            InlineKeyboardButton(
                "📞 Aloqa",
                url=ADMIN_USERNAME
            ),
        ],
    ])


# ==========================================
# BACK BUTTON
# ==========================================

def back_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 Asosiy menyu",
                callback_data="home"
            )
        ]
    ])


# ==========================================
# START
# ==========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = (
        "✨ <b>Assalomu alaykum!</b>\n\n"

        "🤖 <b>ASP Community Bot</b>ga xush kelibsiz!\n\n"

        "🎯 Bu bot orqali ASP Community "
        "haqida ma'lumot olishingiz, Discord "
        "serverimizga kirishingiz va Telegram "
        "kanalimizni kuzatishingiz mumkin.\n\n"

        "👇 <b>Kerakli bo‘limni tanlang:</b>"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# ==========================================
# BUTTON HANDLER
# ==========================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    # ======================================
    # HOME
    # ======================================

    if query.data == "home":

        text = (
            "✨ <b>ASP Community</b>\n\n"
            "🤖 Xush kelibsiz!\n\n"
            "👇 Kerakli bo‘limni tanlang:"
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=main_keyboard(),
        )


    # ======================================
    # PROFILE
    # ======================================

    elif query.data == "profile":

        user = query.from_user

        if user.username:
            username = f"@{user.username}"
        else:
            username = "Username mavjud emas"

        text = (
            "👤 <b>Sizning profilingiz</b>\n\n"

            f"📝 Ism: <b>{user.first_name}</b>\n"

            f"🔗 Username: <b>{username}</b>\n"

            f"🆔 ID: <code>{user.id}</code>\n\n"

            "✅ Profil ma'lumotlari muvaffaqiyatli olindi."
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=back_keyboard(),
        )


    # ======================================
    # HELP
    # ======================================

    elif query.data == "help":

        text = (
            "ℹ️ <b>Yordam</b>\n\n"

            "🤖 <b>Bot komandalar:</b>\n\n"

            "▶️ /start — Asosiy menyu\n"
            "❓ /help — Yordam\n\n"

            "💡 Pastdagi tugmalar orqali "
            "kerakli bo‘limni tanlang."
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=back_keyboard(),
        )


    # ======================================
    # RULES
    # ======================================

    elif query.data == "rules":

        text = (
            "📜 <b>ASP Community qoidalari</b>\n\n"

            "1️⃣ Bir-biringizga hurmat bilan munosabatda bo‘ling.\n"
            "2️⃣ Spam va reklama tarqatmang.\n"
            "3️⃣ Haqorat va janjallarga yo‘l qo‘ymang.\n"
            "4️⃣ Server qoidalariga amal qiling.\n"
            "5️⃣ Adminlar ko‘rsatmalariga rioya qiling.\n\n"

            "🤝 Birgalikda yaxshi community yaratamiz!"
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=back_keyboard(),
        )


# ==========================================
# HELP COMMAND
# ==========================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "ℹ️ <b>ASP Community Bot</b>\n\n"

        "▶️ /start — Asosiy menyu\n"
        "❓ /help — Yordam\n\n"

        "👇 Menyudagi tugmalardan foydalaning.",

        parse_mode="HTML",

        reply_markup=main_keyboard(),
    )


# ==========================================
# MAIN
# ==========================================

def main():

    # --------------------------------------
    # TOKEN
    # --------------------------------------

    token = os.getenv("BOT_TOKEN")

    if not token:

        print("❌ BOT_TOKEN topilmadi!")

        return


    # --------------------------------------
    # HEALTH SERVER
    # --------------------------------------

    health_thread = threading.Thread(
        target=start_health_server,
        daemon=True
    )

    health_thread.start()


    # --------------------------------------
    # TELEGRAM BOT
    # --------------------------------------

    app = Application.builder().token(token).build()


    # Commands
    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("help", help_command)
    )


    # Buttons
    app.add_handler(
        CallbackQueryHandler(button_handler)
    )


    print("====================================")
    print("✅ ASP COMMUNITY BOT IS RUNNING")
    print("🟢 Telegram polling started")
    print("====================================")


    # --------------------------------------
    # RUN
    # --------------------------------------

    app.run_polling(
        drop_pending_updates=True
    )


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":
    main()

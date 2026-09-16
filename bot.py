from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# ASP COMMUNITY LINKS
# =========================

DISCORD_LINK = "https://discord.gg/2bGWXZ6BK"
TELEGRAM_CHANNEL = "https://t.me/asp_community"
ADMIN_USERNAME = "https://t.me/Solh09"


# =========================
# MAIN MENU
# =========================

def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👤 Profil", callback_data="profile"),
            InlineKeyboardButton("ℹ️ Yordam", callback_data="help"),
        ],
        [
            InlineKeyboardButton("🎮 Discord Server", url=DISCORD_LINK),
        ],
        [
            InlineKeyboardButton("📢 Telegram Kanal", url=TELEGRAM_CHANNEL),
        ],
        [
            InlineKeyboardButton("📜 Qoidalar", callback_data="rules"),
            InlineKeyboardButton("📞 Aloqa", url=ADMIN_USERNAME),
        ],
    ])


# =========================
# BACK BUTTON
# =========================

def back_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 Asosiy menyu",
                callback_data="home"
            )
        ]
    ])


# =========================
# /START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "✨ <b>Assalomu alaykum!</b>\n\n"
        "🤖 <b>ASP Community Bot</b>ga xush kelibsiz!\n\n"
        "🎯 Bu bot orqali ASP Community haqida ma'lumot olishingiz, "
        "Discord serverimizga kirishingiz va Telegram kanalimizni kuzatishingiz mumkin.\n\n"
        "👇 <b>Kerakli bo‘limni tanlang:</b>"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    # -------------------------
    # HOME
    # -------------------------

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

    # -------------------------
    # PROFILE
    # -------------------------

    elif query.data == "profile":

        user = query.from_user

        username = (
            f"@{user.username}"
            if user.username
            else "Username mavjud emas"
        )

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

    # -------------------------
    # HELP
    # -------------------------

    elif query.data == "help":

        text = (
            "ℹ️ <b>Yordam</b>\n\n"
            "🤖 <b>Bot komandalar:</b>\n\n"
            "▶️ /start — Asosiy menyu\n"
            "❓ /help — Yordam\n\n"
            "💡 Tugmalar orqali barcha asosiy bo‘limlardan foydalanishingiz mumkin."
        )

        await query.edit_message_text(
            text,
            parse_mode="HTML",
            reply_markup=back_keyboard(),
        )

    # -------------------------
    # RULES
    # -------------------------

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


# =========================
# /HELP
# =========================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    await update.message.reply_text(
        "ℹ️ <b>Yordam</b>\n\n"
        "▶️ /start — Asosiy menyu\n"
        "❓ /help — Yordam\n\n"
        "👇 Menyudagi tugmalardan foydalaning.",
        parse_mode="HTML",
        reply_markup=main_keyboard(),
    )


# =========================
# BOT START
# =========================

def main():

    token = input("BOT TOKENNI kiriting: ").strip()

    if not token:
        print("❌ Token kiritilmadi.")
        return

    app = Application.builder().token(token).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Buttons
    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    print("✅ ASP Community Bot ishga tushdi!")
    print("📱 Telegram orqali /start yuboring.")
    print("🟢 Bot ishlayapti...")

    app.run_polling()


# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()
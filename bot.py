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


# ==================================================
# SOZLAMALAR
# ==================================================

DISCORD_LINK = "https://discord.gg/G4EMM8GkH"
TELEGRAM_CHANNEL = "https://t.me/asp_community"
CHANNEL_USERNAME = "@asp_community"
ADMIN_USERNAME = "https://t.me/Solh09"

BANNER_FILE = "asp_banner.png"


# ==================================================
# RENDER HEALTH CHECK
# ==================================================

class HealthHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ASP Community Bot Online!")

    def log_message(self, format, *args):
        return


def run_health_server():
    port = int(os.environ.get("PORT", 10000))

    server = HTTPServer(
        ("0.0.0.0", port),
        HealthHandler
    )

    print(f"🌐 Health server started on port {port}")

    server.serve_forever()


# ==================================================
# MAJBURIY OBUNA TUGMALARI
# ==================================================

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


# ==================================================
# ASOSIY MENU
# ==================================================

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
            )
        ],

        [
            InlineKeyboardButton(
                "🎮 Discord Server",
                url=DISCORD_LINK
            )
        ],

        [
            InlineKeyboardButton(
                "📢 Telegram Kanal",
                url=TELEGRAM_CHANNEL
            )
        ],

        [
            InlineKeyboardButton(
                "📜 Qoidalar",
                callback_data="rules"
            ),
            InlineKeyboardButton(
                "📞 Aloqa",
                url=ADMIN_USERNAME
            )
        ]

    ])


# ==================================================
# OBUNANI TEKSHIRISH
# ==================================================

async def is_subscribed(bot, user_id):

    try:

        member = await bot.get_chat_member(
            chat_id=CHANNEL_USERNAME,
            user_id=user_id
        )

        if member.status in (
            "member",
            "administrator",
            "creator"
        ):
            return True

        if member.status == "restricted":
            return getattr(member, "is_member", False)

        return False

    except Exception as e:

        print(f"❌ Subscription check error: {e}")

        return False


# ==================================================
# WELCOME MATNI
# ==================================================

def welcome_text(user):

    return (
        f"👋 <b>Assalomu alaykum, {user.first_name}!</b>\n\n"

        "🤖 <b>ASP Community Bot</b>ga xush kelibsiz!\n\n"

        "💙 Bizning community bilan birga bo‘ling.\n\n"

        "🎮 <b>Discord</b> — do‘stlaringiz bilan suhbatlashing.\n"
        "📢 <b>Telegram</b> — yangiliklardan xabardor bo‘ling.\n\n"

        "━━━━━━━━━━━━━━━━━━\n"
        "👑 <b>ASP COMMUNITY</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"

        "👇 Kerakli bo‘limni tanlang:"
    )


# ==================================================
# OBUNA KERAK XABARI
# ==================================================

def subscription_text():

    return (
        "👋 <b>Assalomu alaykum!</b>\n\n"

        "🤖 <b>ASP Community Bot</b>ga xush kelibsiz!\n\n"

        "📢 Botdan foydalanish uchun avval "
        "<b>ASP Community</b> kanaliga obuna bo‘ling.\n\n"

        "✅ Obuna bo‘lganingizdan keyin "
        "<b>«Obunani tekshirish»</b> tugmasini bosing."
    )


# ==================================================
# START
# ==================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    # ----------------------------------------------
    # OBUNA YO‘Q
    # ----------------------------------------------

    if not await is_subscribed(
        context.bot,
        user.id
    ):

        await update.message.reply_photo(

            photo=open(BANNER_FILE, "rb"),

            caption=subscription_text(),

            parse_mode="HTML",

            reply_markup=subscription_keyboard()
        )

        return

    # ----------------------------------------------
    # OBUNA BOR
    # ----------------------------------------------

    await update.message.reply_photo(

        photo=open(BANNER_FILE, "rb"),

        caption=welcome_text(user),

        parse_mode="HTML",

        reply_markup=main_keyboard()
    )


# ==================================================
# HELP COMMAND
# ==================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.effective_user

    if not await is_subscribed(
        context.bot,
        user.id
    ):

        await update.message.reply_text(

            subscription_text(),

            parse_mode="HTML",

            reply_markup=subscription_keyboard()
        )

        return

    text = (
        "ℹ️ <b>ASP Community Yordam</b>\n\n"

        "👤 <b>Profil</b> — profilingiz haqida ma'lumot.\n\n"

        "🎮 <b>Discord</b> — ASP Community Discord serveri.\n\n"

        "📢 <b>Telegram</b> — ASP Community Telegram kanali.\n\n"

        "📜 <b>Qoidalar</b> — community qoidalari.\n\n"

        "📞 <b>Aloqa</b> — administrator bilan bog‘lanish."
    )

    await update.message.reply_text(

        text,

        parse_mode="HTML",

        reply_markup=main_keyboard()
    )


# ==================================================
# BUTTON HANDLER
# ==================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    user = query.from_user

    # ==================================================
    # OBUNANI TEKSHIRISH
    # ==================================================

    if query.data == "check_subscription":

        subscribed = await is_subscribed(
            context.bot,
            user.id
        )

        # ----------------------------------------------
        # OBUNA BOR
        # ----------------------------------------------

        if subscribed:

            await query.answer(
                "✅ Obuna tasdiqlandi!"
            )

            await query.edit_message_caption(

                caption=welcome_text(user),

                parse_mode="HTML",

                reply_markup=main_keyboard()
            )

        # ----------------------------------------------
        # OBUNA YO‘Q
        # ----------------------------------------------

        else:

            await query.answer(

                "❌ Avval Telegram kanalga obuna bo‘ling!",

                show_alert=True
            )

        return

    # ==================================================
    # QOLGAN TUGMALAR UCHUN OBUNA TEKSHIRISH
    # ==================================================

    if not await is_subscribed(
        context.bot,
        user.id
    ):

        await query.answer(

            "❌ Avval kanalga obuna bo‘ling!",

            show_alert=True
        )

        return

    # ==================================================
    # HOME
    # ==================================================

    if query.data == "home":

        await query.answer()

        await query.edit_message_caption(

            caption=welcome_text(user),

            parse_mode="HTML",

            reply_markup=main_keyboard()
        )

    # ==================================================
    # PROFILE
    # ==================================================

    elif query.data == "profile":

        await query.answer()

        text = (
            "👤 <b>Profil</b>\n\n"

            f"🆔 ID: <code>{user.id}</code>\n"

            f"👤 Ism: {user.first_name}\n"
        )

        if user.username:

            text += (
                f"🔗 Username: @{user.username}\n"
            )

        text += "\n💙 <b>ASP Community</b>"

        await query.edit_message_caption(

            caption=text,

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

    # ==================================================
    # HELP
    # ==================================================

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

        await query.edit_message_caption(

            caption=text,

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

    # ==================================================
    # RULES
    # ==================================================

    elif query.data == "rules":

        await query.answer()

        text = (
            "📜 <b>ASP Community Qoidalari</b>\n\n"

            "1️⃣ Bir-biringizni hurmat qiling.\n\n"
            "2️⃣ Spam va flood taqiqlanadi.\n\n"
            "3️⃣ Reklama faqat ruxsat bilan.\n\n"
            "4️⃣ Haqorat va toxic xatti-harakatlarga "
            "yo‘l qo‘yilmaydi.\n\n"
            "5️⃣ Administratorlar qaroriga rioya qiling.\n\n"

            "🤝 <b>Hammaga yaxshi muhit yaratamiz!</b>"
        )

        await query.edit_message_caption(

            caption=text,

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


# ==================================================
# MAIN
# ==================================================

def main():

    token = os.environ.get("BOT_TOKEN")

    if not token:

        print("❌ BOT_TOKEN topilmadi!")

        return

    # ----------------------------------------------
    # RENDER SERVER
    # ----------------------------------------------

    threading.Thread(

        target=run_health_server,

        daemon=True

    ).start()

    # ----------------------------------------------
    # TELEGRAM BOT
    # ----------------------------------------------

    application = (
        Application
        .builder()
        .token(token)
        .build()
    )

    # START
    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    # HELP
    application.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    # BUTTONS
    application.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    print("🤖 ASP Community Bot ishga tushdi!")

    # ----------------------------------------------
    # POLLING
    # ----------------------------------------------

    application.run_polling(
        drop_pending_updates=True
    )


# ==================================================
# RUN
# ==================================================

if __name__ == "__main__":

    main()

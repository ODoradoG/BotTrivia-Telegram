from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from utils.translations import t

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    keyboard = [
        [InlineKeyboardButton("⚽ Sports", callback_data="tema_esports")],
        [InlineKeyboardButton("🔬 Science", callback_data="tema_ciencia")],
        [InlineKeyboardButton("📜 History", callback_data="tema_historia")],
        [InlineKeyboardButton("🌐 Change language", callback_data="language")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(t("start_welcome", lang), reply_markup=reply_markup)

async def seleccionar_tema_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tema = query.data.replace("tema_", "")
    context.user_data["tema"] = tema
    lang = context.user_data.get("lang", "en")
    await query.edit_message_text(t("choose_topic", lang, topic=tema.capitalize()))

def start():
    return CommandHandler("start", start_command)

def seleccionar_tema():
    return CallbackQueryHandler(seleccionar_tema_callback, pattern="^tema_")

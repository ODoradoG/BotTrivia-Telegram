from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes
from utils.translations import t

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    keyboard = [
        [InlineKeyboardButton(t("change_language", lang), callback_data="language")],
        [InlineKeyboardButton(t("select_topic", lang), callback_data="topic")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message or update.callback_query.message
    await message.reply_text(t("start_welcome", lang), reply_markup=reply_markup)



def start():
    return CommandHandler("start", start_command)


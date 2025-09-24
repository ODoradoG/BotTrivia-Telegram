import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from utils.translations import t
from commands.start import start_command

async def theme_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")

    if query.data == "topic":
        keyboard = [
            [InlineKeyboardButton(t("sport_topic", lang), callback_data="tema_esports")],
            [InlineKeyboardButton(t("science_topic", lang), callback_data="tema_ciencia")],
            [InlineKeyboardButton(t("history_topic", lang), callback_data="tema_historia")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(t("select_topic", lang), reply_markup=reply_markup)
        return
    
    tema = query.data.replace("tema_", "")
    context.user_data["tema"] = tema
    await query.edit_message_text(t("choose_topic", lang, topic=tema.capitalize()))

def theme():
    return CallbackQueryHandler(theme_callback, pattern="^(topic|tema_)")


import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from utils.translations import t
from utils.api import get_tema
from commands.start import start_command

async def theme_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = context.user_data.get("lang", "en")

    if query.data == "topic":
        keyboard = [
            [InlineKeyboardButton(t("sports_topic", lang), callback_data="tema_esports")],
            [InlineKeyboardButton(t("science_topic", lang), callback_data="tema_ciencia")],
            [InlineKeyboardButton(t("history_topic", lang), callback_data="tema_historia")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(t("select_topic", lang), reply_markup=reply_markup)
        return
    
    tema = query.data.replace("tema_", "")
    context.user_data["tema"] = tema
    tema_trans = context.user_data.get("tema")
    temas = get_tema(tema_trans)
    tema_translation = t(f"{temas}_topic", lang) if temas else tema 
    await query.edit_message_text(t("choose_topic", lang, topic=tema_translation))

def theme():
    return CallbackQueryHandler(theme_callback, pattern="^(topic|tema_)")


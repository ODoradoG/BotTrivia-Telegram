import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ContextTypes
from utils.translations import t
from commands.start import start_command

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "language":
        keyboard = [
            [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
            [InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")],
            [InlineKeyboardButton("🇦🇩 Català", callback_data="lang_ca")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 Select language / Selecciona idioma / Selecciona llengua:", reply_markup=reply_markup)
        return

    new_lang = query.data.replace("lang_", "")
    context.user_data["lang"] = new_lang
    await query.edit_message_text(t("finally_message", new_lang))
    await asyncio.sleep(3)
    await start_command(update, context)

def language():
    return CallbackQueryHandler(language_callback, pattern="^(language|lang_)")

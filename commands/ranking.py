from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.score import puntuacions
from utils.translations import t

from utils.api import temes, get_tema

async def ranking_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema_usuario = context.user_data.get("tema")
    lang = context.user_data.get("lang", "en")
    if not tema_usuario:
        await update.message.reply_text(t("no_topic", lang))
        return

    tema = get_tema(tema_usuario)
    if not tema:
        await update.message.reply_text(t("no_topic", lang))
        return

    classificacio = sorted(
        [(p["nom"], p["temes"].get(tema, 0)) for p in puntuacions.values()],
        key=lambda x: x[1],
        reverse=True
    )

    tema_translation = t(f"{tema}_topic", lang)
    text = t("ranking", lang) + f" ({tema_translation})\n\n"

    for i, (nom, punts) in enumerate(classificacio, 1):
        text += f"{i}. {nom} - {punts} punts\n"

    if not classificacio:
        text += t("no_scores", lang)

    await update.message.reply_text(text)


def ranking():
    return CommandHandler("ranking", ranking_command)

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.score import puntuacions
from utils.api import temes

async def ranking_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tema = context.user_data.get("tema")
    if not tema:
        await update.message.reply_text("❗ Primer has de triar un tema amb /start")
        return

    classificacio = sorted(
        [(p["nom"], p["temes"][tema]) for p in puntuacions.values()],
        key=lambda x: x[1], reverse=True
    )
    text = f"🏆 Classificació ({tema.capitalize()}):\n"
    for i, (nom, punts) in enumerate(classificacio, 1):
        text += f"{i}. {nom} - {punts} punts\n"

    await update.message.reply_text(text)

def ranking():
    return CommandHandler("ranking", ranking_command)

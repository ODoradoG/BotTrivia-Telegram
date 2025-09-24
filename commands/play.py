import requests, random
from googletrans import Translator
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, ContextTypes
from utils.api import temes, imatges
from utils.score import puntuacions
from utils.translations import t, translate_text
translator = Translator()
async def play_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    tema = context.user_data.get("tema")
    if not tema:
        await update.message.reply_text(t("no_topic", lang))
        return

    categoria = temes[tema]
    url = f"https://opentdb.com/api.php?amount=1&category={categoria}&type=multiple"
    data = requests.get(url).json()
    pregunta = data["results"][0]["question"]
    correcta = data["results"][0]["correct_answer"]
    incorrectes = data["results"][0]["incorrect_answers"]

    if lang != "en":
        pregunta = translator.translate(pregunta, dest=lang).text
        correcta = translator.translate(correcta, dest=lang).text
        incorrectes = [translator.translate(ans, dest=lang).text for ans in incorrectes]


    opcions = incorrectes + [correcta]
    random.shuffle(opcions)

    context.user_data["correcta"] = correcta
    context.user_data["opcions"] = opcions
    context.user_data["tema_actual"] = tema

    text = f"❓ {pregunta}\n\n"
    for i, opcio in enumerate(opcions, 1):
        text += f"{i}. {opcio}\n"

    keyboard = [
        [InlineKeyboardButton("1️⃣", callback_data="resposta_0"),
         InlineKeyboardButton("2️⃣", callback_data="resposta_1")],
        [InlineKeyboardButton("3️⃣", callback_data="resposta_2"),
         InlineKeyboardButton("4️⃣", callback_data="resposta_3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(photo=imatges[tema], caption=text, reply_markup=reply_markup)

async def resposta_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    index = int(query.data.split("_")[1])
    eleccio = context.user_data["opcions"][index]
    correcta = context.user_data["correcta"]
    tema = context.user_data["tema_actual"]
    lang = context.user_data.get("lang", "en")

    user_id = query.from_user.id
    user_name = query.from_user.first_name

    if user_id not in puntuacions:
        puntuacions[user_id] = {"nom": user_name, "temes": {t: 0 for t in temes}}

    if eleccio == correcta:
        puntuacions[user_id]["temes"][tema] += 1
        text = t("correct", lang, points=puntuacions[user_id]["temes"][tema], topic=tema.capitalize())
    else:
        text = t("incorrect", lang, answer=correcta)

    await query.edit_message_caption(caption=text)

def play():
    return CommandHandler("play", play_command)

def resposta():
    return CallbackQueryHandler(resposta_callback, pattern="^resposta_")

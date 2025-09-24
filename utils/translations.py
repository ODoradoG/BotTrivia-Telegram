import requests

translations = {
    "start_welcome": {
        "en": "🎮 Welcome to TriviaBot!\nChoose a topic or change language:",
        "es": "🎮 ¡Bienvenido a TriviaBot!\nElige un tema o cambia el idioma:",
        "ca": "🎮 Benvingut al TriviaBot!\nTria un tema o canvia l'idioma:"
    },
    "finally_message": {
        "en": "✅ Language changed!",
        "es": "✅ Lenguaje cambiado!",
        "ca": "✅ Llenguatge canviat! "
    },
    "change_language": {
        "en": "🌐 Change language",
        "es": "🌐 Cambiar idioma",
        "ca": "🌐 Canviar l'idioma"
    },
    "select_topic": {
        "en": "🧩 Select a topic.",
        "es": "🧩 Selecciona un tema.",
        "ca": "🧩 Tria un tema"
    },
    "choose_topic": {
        "en": "✅ You chose the topic: {topic}\nType /play to start!",
        "es": "✅ Has elegido el tema: {topic}\nEscribe /play para empezar!",
        "ca": "✅ Has triat el tema: {topic}\nEscriu /play per començar!"
    },
    "sport_topic": {
        "en:": "⚽ Sports",
        "es": "⚽ Deportes",
        "ca": "⚽ Esports"
    },
    "science_topic": {
        "en:": "🔬 Science",
        "es": "🔬 Ciencia",
        "ca": "🔬 Ciència"
    },
    "history_topic": {
        "en:": "📜 History",
        "es": "📜 Historia",
        "ca": "📜 Història"
    },
    "no_topic": {
        "en": "❗ You must first choose a topic with /start",
        "es": "❗ Primero debes elegir un tema con /start",
        "ca": "❗ Primer has de triar un tema amb /start"
    },
    "correct": {
        "en": "✅ Correct! 🎉 You have {points} points in {topic}.",
        "es": "✅ ¡Correcto! 🎉 Tienes {points} puntos en {topic}.",
        "ca": "✅ Correcte! 🎉 Tens {points} punts en {topic}."
    },
    "incorrect": {
        "en": "❌ Wrong! The answer was: {answer}",
        "es": "❌ ¡Incorrecto! La respuesta era: {answer}",
        "ca": "❌ Incorrecte! La resposta era: {answer}"
    },
    "ranking": {
        "en": "🏆 Ranking ({topic}):\n",
        "es": "🏆 Clasificación ({topic}):\n",
        "ca": "🏆 Classificació ({topic}):\n"
    }
}

def t(key, lang="en", **kwargs):
    text = translations.get(key, {}).get(lang, "")
    return text.format(**kwargs)

def translate_text(text, lang):
    lang_map = {"en": "en", "es": "es", "ca": "ca"}
    target = lang_map.get(lang, "en")
    if target == "en":
        return text
    try:
        resp = requests.post(
            "https://libretranslate.de/translate",
            data={"q": text, "source": "en", "target": target}
        )
        return resp.json()["translatedText"]
    except:
        return text

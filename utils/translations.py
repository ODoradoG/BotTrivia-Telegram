import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

translations = {
    "start_welcome": {
        "en": "🎮 Welcome to TriviaBot!\nChoose a topic or change language:",
        "es": "🎮 ¡Bienvenido a TriviaBot!\nElige un tema o cambia el idioma:",
        "ca": "🎮 Benvingut al TriviaBot!\nTria un tema o canvia l'idioma:"
    },
    "finally_message": {
        "en": "✅ Language changed!",
        "es": "✅ Lenguaje cambiado!",
        "ca": "✅ Llenguatge canviat!"
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
    "sports_topic": { "en": "⚽ Sports", "es": "⚽ Deportes", "ca": "⚽ Esports" },
    "science_topic": { "en": "🔬 Science", "es": "🔬 Ciencia", "ca": "🔬 Ciència" },
    "history_topic": { "en": "📜 History", "es": "📜 Historia", "ca": "📜 Història" },

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
        "en": "🏆 Ranking ",
        "es": "🏆 Clasificación ",
        "ca": "🏆 Classificació "
    }, 
    "retry":{
        "en": "🔁 If you want to play more use /play or if you want to change de topic then /start",
        "es": "🔁 Si quieres jugar otra vez use /play o si quieres cambiar el topico usa /start",
        "ca": "🔁 Si vols jugar un altre cop utilitza /play o si vols canviar el topic utilitza /start"
    }
}

def t(key, lang="en", **kwargs):
    text = translations.get(key, {}).get(lang, "")
    return text.format(**kwargs)

def translate_text(text, target_lang):
    """
    Translate text with multiple fallback options and better error handling
    """
    if target_lang == "en":
        return text
    
    lang_map = {"en": "en", "es": "es", "ca": "ca"}
    target = lang_map.get(target_lang, "en")
    
    if target == "en":
        return text
    
    translation_services = [
        _translate_with_mymemory,
        _translate_with_google_translate_api
    ]
    
    for service in translation_services:
        try:
            result = service(text, "en", target)
            if result and result != text:  
                logger.info(f"Successfully translated with {service.__name__}")
                return result
        except Exception as e:
            logger.warning(f"Translation failed with {service.__name__}: {e}")
            continue
    
    logger.error(f"All translation services failed for text: {text[:50]}...")
    return text


def _translate_with_mymemory(text, source_lang, target_lang):
    """Try MyMemory translation service"""
    lang_mapping = {"ca": "ca-es", "es": "es", "en": "en"}
    target_mapped = lang_mapping.get(target_lang, target_lang)
    
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"{source_lang}|{target_mapped}"
    }
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    
    result = response.json()
    if result.get("responseStatus") == 200:
        return result["responseData"]["translatedText"]
    else:
        raise Exception(f"MyMemory API error: {result.get('responseDetails', 'Unknown error')}")

def _translate_with_google_translate_api(text, source_lang, target_lang):
    """Try Google Translate API (free endpoint)"""
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_lang,
        "tl": target_lang,
        "dt": "t",
        "q": text
    }
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    
    result = response.json()
    if result and result[0] and result[0][0]:
        return result[0][0][0]
    else:
        raise Exception("Invalid response from Google Translate")
def test_translation():
    """Test the translation functionality"""
    test_cases = [
        ("Hello world", "es"),
        ("Hello world", "ca"),
        ("Science", "es"),
        ("Science", "ca")
    ]
    
    for text, lang in test_cases:
        result = translate_text(text, lang)
        print(f"'{text}' -> {lang}: '{result}'")

if __name__ == "__main__":
    test_translation()
import os
from dotenv import load_dotenv
from telegram.ext import Application
from commands.start import start
from commands.play import play, resposta
from commands.ranking import ranking
from commands.language import language
from commands.theme import theme

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    if not TOKEN:
        raise ValueError("❌ No se encontró TELEGRAM_TOKEN en el archivo .env")
    
    app = Application.builder().token(TOKEN).build()

    app.add_handler(start())
    app.add_handler(theme())
    app.add_handler(language())
    app.add_handler(play())
    app.add_handler(resposta())
    app.add_handler(ranking())

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()

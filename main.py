from telegram.ext import Application
from commands.start import start
from commands.play import play, resposta
from commands.ranking import ranking
from commands.language import language
from commands.theme import theme

TOKEN = "8437974418:AAGq6QP-n1stlE9THHLb33KkA_Im3DCmjfk"

def main():
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

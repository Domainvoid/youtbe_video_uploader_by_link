import json
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from reels_shorts_downloader import urlinput

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Load the token from the config file
with open("config.json", "r") as file:
    Token = json.load(file)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )
    logging.info(f"User {user.name} started the bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")
    logging.info("Help command invoked.")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.text
    lst = ["https://youtube.com", "https://www.instagram.com", "https"]

    if any(url in msg for url in lst):
        # Process the URL
        urlinput(msg)
        logging.info(f"Processing URL: {msg}")
    else:
        await update.message.reply_text("Please send a valid URL!")
        logging.warning(f"Invalid URL received: {msg}")

def main() -> None:
    application = Application.builder().token(Token["token"]).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logging.info("Bot started.")

if __name__ == "__main__":
    main()

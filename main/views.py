from telegram import Update
from telegram.ext import CallbackContext

def start_handler(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello, I'm your new bot!")
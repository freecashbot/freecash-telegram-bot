import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
REF_LINK = os.getenv("REF_LINK", "https://freecash.com/r/153982591160")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Welcome to Freecash Bot!\n\n"
        f"Start earning: {REF_LINK}\n\n"
        f"Commands:\n"
        f"/offers - latest offers\n"
        f"/balance - check balance\n"
        f"/withdraw - how to withdraw"
    )

def offers(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"Top offers:\n"
        f"• Install apps\n"
        f"• Register on websites\n"
        f"• Play games\n\n"
        f"Offers: {REF_LINK}"
    )

def balance(update: Update, context: CallbackContext):
    update.message.reply_text(f"Check your Freecash balance:\n{REF_LINK}")

def withdraw(update: Update, context: CallbackContext):
    update.message.reply_text(f"You can withdraw from $0.50 via PayPal, crypto, Steam, Amazon.\n{REF_LINK}")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("offers", offers))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("withdraw", withdraw))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

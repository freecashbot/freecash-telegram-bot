import os
import json
import threading
import time
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
REF_LINK = os.getenv("REF_LINK", "https://freecash.com/r/153982591160")
USER_LOG = "users.json"

def load_users():
    if os.path.exists(USER_LOG):
        with open(USER_LOG, "r") as f:
            return json.load(f)
    return {}

def save_user(user_id, username):
    users = load_users()
    if str(user_id) not in users:
        users[str(user_id)] = {
            "username": username,
            "joined": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(USER_LOG, "w") as f:
            json.dump(users, f, indent=2)

def delayed_message(context: CallbackContext, chat_id: int, delay: int):
    def job():
        time.sleep(delay)
        context.bot.send_message(
            chat_id=chat_id,
            text="🎯 Не забудь заработать $5 прямо сейчас — начни с любого задания на Freecash!",
            parse_mode=ParseMode.HTML
        )
    threading.Thread(target=job).start()

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    save_user(user.id, user.username or "unknown")

    welcome_text = (
        f"👋 <b>Welcome to Freecash Bot!</b>\n\n"
        f"💸 <a href='{REF_LINK}'>Start earning money here</a>\n\n"
        f"🛠 Commands:\n"
        f"/offers - latest offers\n"
        f"/balance - check your balance\n"
        f"/withdraw - withdrawal options\n"
        f"/invite - get your referral link"
    )

    update.message.reply_text(welcome_text, parse_mode=ParseMode.HTML)
    delayed_message(context, update.effective_chat.id, delay=300)

def offers(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"🔥 <b>Top earning tasks:</b>\n"
        f"• Install apps\n"
        f"• Register on websites\n"
        f"• Play games\n\n"
        f"➡️ <a href='{REF_LINK}'>Start earning on Freecash</a>",
        parse_mode=ParseMode.HTML
    )

def balance(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"💰 Check your Freecash balance here:\n{REF_LINK}"
    )

def withdraw(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"💸 You can withdraw from $0.50 via PayPal, Bitcoin, Ethereum, Steam, Amazon and more.\n"
        f"Link: {REF_LINK}"
    )

def invite(update: Update, context: CallbackContext):
    update.message.reply_text(
        f"📢 Invite friends and earn lifetime bonuses!\n\n"
        f"Your referral link:\n{REF_LINK}"
    )

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("offers", offers))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("withdraw", withdraw))
    dp.add_handler(CommandHandler("invite", invite))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
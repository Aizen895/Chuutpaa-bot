 # bot.py (Main Bot Logic)
import .utils
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
import utils
import keep_alive  # Import the keep_alive module

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Environment Variables (Set in Koyeb)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")  # Where to send scheduled news
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")

# Telegram bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your auto anime news bot.")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_items = utils.get_anime_news()
    if news_items:
        message = "Here's the latest anime news:\n"
        for item in news_items:
            message += f"- <a href='{item['link']}'>{item['title']}</a>\n"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode="HTML")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't fetch the news right now.")

# Scheduler Function
async def send_scheduled_news(context: ContextTypes.DEFAULT_TYPE):
    news_items = utils.get_anime_news()
    if news_items:
        message = "Daily Anime News:\n"
        for item in news_items:
            message += f"- <a href='{item['link']}'>{item['title']}</a>\n"
        try:
            await context.bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="HTML") # send msg to chat id
        except Exception as e:
            logging.error(f"Error sending scheduled message: {e}")
    else:
        logging.warning("Couldn't fetch news for scheduled update.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    news_handler = CommandHandler('news', news)
    application.add_handler(start_handler)
    application.add_handler(news_handler)

    # Set up scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_scheduled_news, 'interval', hours=6, args=[ContextTypes.DEFAULT_TYPE])  # Send every 6 hours
    scheduler.start()

    keep_alive.keep_alive()  # Start the web server for UptimeRobot
    application.run_polling()

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.environ.get("BOT_TOKEN")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hello there! Welcome to *ZX Watermark Removal Bot* 💖\n\n"
        "✨ I can help you *ADD* and *REMOVE* watermarks from PDF files!\n\n"
        "📂 *Supported files:*\n"
        "• PDF documents only\n\n"
        "⚡ *Commands:*\n"
        "• /addwatermark – Add watermark to PDF\n"
        "• /removewatermark – Remove watermark from PDF\n\n"
        "😊 Send a command to get started!",
        parse_mode="Markdown"
    )

# /addwatermark
async def add_watermark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 Sure! Send me your *PDF file* for adding a watermark ✨",
        parse_mode="Markdown"
    )

# /removewatermark
async def remove_watermark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧹 Send your *PDF file* to remove the watermark ✨",
        parse_mode="Markdown"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addwatermark", add_watermark))
app.add_handler(CommandHandler("removewatermark", remove_watermark))

app.run_polling()

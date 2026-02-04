from telegram import Update, Document
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os

TOKEN = os.environ.get("BOT_TOKEN")

# start
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

# flags to know what user wants
async def addwatermark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "add"
    await update.message.reply_text(
        "📄 Sure! Send me your *PDF file* for adding a watermark ✨",
        parse_mode="Markdown"
    )

async def removewatermark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "remove"
    await update.message.reply_text(
        "🧹 Send your *PDF file* to remove the watermark ✨",
        parse_mode="Markdown"
    )

# handle PDF
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")

    if not mode:
        await update.message.reply_text("❗ First use /addwatermark or /removewatermark")
        return

    doc: Document = update.message.document

    file = await doc.get_file()
    input_path = f"{doc.file_name}"
    output_path = doc.file_name.replace(".pdf", "_cleaned.pdf")

    await file.download_to_drive(input_path)

    # 🔥 DEMO processing (real logic baad me)
    os.rename(input_path, output_path)

    await update.message.reply_document(
        document=open(output_path, "rb"),
        caption="✅ Done! Watermark process completed 🎉"
    )

    os.remove(output_path)
    context.user_data.clear()

# app
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addwatermark", addwatermark))
app.add_handler(CommandHandler("removewatermark", removewatermark))
app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

app.run_polling()

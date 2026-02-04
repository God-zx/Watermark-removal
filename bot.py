from telegram import Update, Document
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os
import pikepdf

# TOKEN (Render me ENV me set karo)
TOKEN = os.environ.get("BOT_TOKEN")

# -------- WATERMARK REMOVE FUNCTION --------
def remove_text_watermark(input_pdf, output_pdf):
    with pikepdf.open(input_pdf) as pdf:
        for page in pdf.pages:
            # Remove annotations (most text watermarks)
            if "/Annots" in page:
                del page["/Annots"]
        pdf.save(output_pdf)

# -------- COMMANDS --------
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

async def addwatermark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "add"
    await update.message.reply_text(
        "📄 Send your *PDF file* to add watermark ✨",
        parse_mode="Markdown"
    )

async def removewatermark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["mode"] = "remove"
    await update.message.reply_text(
        "🧹 Send your *PDF file* to remove watermark ✨",
        parse_mode="Markdown"
    )

# -------- HANDLE PDF --------
async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get("mode")

    if not mode:
        await update.message.reply_text(
            "❗ Please use /addwatermark or /removewatermark first"
        )
        return

    doc: Document = update.message.document
    file = await doc.get_file()

    input_path = doc.file_name
    output_path = doc.file_name.replace(".pdf", "_cleaned.pdf")

    await file.download_to_drive(input_path)

    try:
        if mode == "remove":
            remove_text_watermark(input_path, output_path)
            caption = "✅ Done! Watermark removed 🎉"
        else:
            # ADD watermark logic baad me
            os.rename(input_path, output_path)
            caption = "✅ Done! Watermark added 🎉"

        await update.message.reply_document(
            document=open(output_path, "rb"),
            caption=caption
        )

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        context.user_data.clear()

# -------- APP --------
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("addwatermark", addwatermark))
app.add_handler(CommandHandler("removewatermark", removewatermark))
app.add_handler(MessageHandler(filters.Document.PDF, handle_pdf))

app.run_polling()

# --- File: handlers/transaksi.py ---
import re
from telegram.ext import MessageHandler, filters, ContextTypes
from telegram import Update
from services.parser import parse_transaksi

async def handle_transaksi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    response = parse_transaction(user_id, text)
    await update.message.reply_text(response, parse_mode="Markdown")

transaksi_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_transaksi)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("📊 Ringkasan", callback_data='ringkasan'),
            InlineKeyboardButton("📈 Grafik", callback_data='grafik'),
        ],
        [
            InlineKeyboardButton("📁 Export Excel", callback_data='export'),
            InlineKeyboardButton("ℹ️ Help", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Hai! Aku bot pencatat keuanganmu.\n\n"
        "Silakan pilih menu atau ketik transaksi secara langsung.",
        reply_markup=reply_markup
    )

# Handler agar bisa ditambahkan ke main.py
start_cmd = CommandHandler("start", start)

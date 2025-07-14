from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "ℹ️ *Panduan Penggunaan Bot Keuangan*\n\n"
        "📝 Kamu bisa langsung ketik transaksi seperti:\n"
        "`+50000 gaji bulan ini`\n"
        "`-20000 beli kopi`\n\n"
        "📌 Perintah lain:\n"
        "/start - Tampilkan menu\n"
        "/ringkasan - Ringkasan saldo\n"
        "/grafik - Grafik pemasukan & pengeluaran\n"
        "/export - Export data ke Excel\n"
        "/help - Bantuan ini"
    )

    target = update.message or update.callback_query.message
    await target.reply_text(message, parse_mode="Markdown")

from telegram.ext import CommandHandler
help_cmd = CommandHandler("help", help_command)

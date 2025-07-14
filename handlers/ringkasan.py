import sqlite3
from telegram import Update
from telegram.ext import ContextTypes

async def ringkasan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("keuangan.db")
    c = conn.cursor()

    c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'pemasukan'", (user_id,))
    total_pemasukan = c.fetchone()[0] or 0

    c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'pengeluaran'", (user_id,))
    total_pengeluaran = c.fetchone()[0] or 0

    total = total_pemasukan - total_pengeluaran

    conn.close()

    message = (
        f"📊 *Ringkasan Keuangan*\n\n"
        f"📥 Total Pemasukan: Rp {total_pemasukan:,.0f}\n"
        f"📤 Total Pengeluaran: Rp {total_pengeluaran:,.0f}\n"
        f"💰 Saldo Akhir: Rp {total:,.0f}"
    )

    target = update.message or update.callback_query.message
    await target.reply_text(message, parse_mode="Markdown")

from telegram.ext import CommandHandler
ringkasan_cmd = CommandHandler("ringkasan", ringkasan)

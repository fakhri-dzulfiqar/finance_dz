import sqlite3
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def ringkasan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("keuangan.db")
    c = conn.cursor()

    # ✅ Ganti 'pemasukan' -> 'masuk'
    c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'masuk'", (user_id,))
    total_pemasukan = c.fetchone()[0] or 0

    # ✅ Ganti 'pengeluaran' -> 'keluar'
    c.execute("SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'keluar'", (user_id,))
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

ringkasan_cmd = CommandHandler("ringkasan", ringkasan)

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from services.database import get_transactions_between
from services.utils import format_rp
from datetime import datetime, timedelta

def summarize(transactions):
    masuk = sum(t[2] for t in transactions if t[1] == 'masuk')
    keluar = sum(t[2] for t in transactions if t[1] == 'keluar')
    saldo = masuk - keluar
    return masuk, keluar, saldo

async def laporan_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    arg = context.args[0] if context.args else "minggu"

    if arg.lower() == "bulan":
        end = datetime.now()
        start = end.replace(day=1)
        periode = "📅 *Laporan Bulan Ini*"
    else:
        end = datetime.now()
        start = end - timedelta(days=7)
        periode = "🗓️ *Laporan Mingguan*"

    data = get_transactions_between(user_id, start, end)
    masuk, keluar, saldo = summarize(data)

    msg = f"""{periode}
🟢 Pemasukan: {format_rp(masuk)}
🔴 Pengeluaran: {format_rp(keluar)}
💰 Saldo Bersih: {format_rp(saldo)}"""

    await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

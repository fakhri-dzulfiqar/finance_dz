# grafik.py
import matplotlib.pyplot as plt
from datetime import datetime
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes, CommandHandler
from io import BytesIO
from services.database import c  # GANTI: pakai cursor dari services

async def grafik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    c.execute("""
        SELECT DATE(timestamp), 
               SUM(CASE WHEN type='masuk' THEN amount ELSE 0 END),
               SUM(CASE WHEN type='keluar' THEN amount ELSE 0 END)
        FROM transactions
        WHERE user_id = ?
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp)
    """, (user_id,))
    data = c.fetchall()

    if not data:
        target = update.message or update.callback_query.message
        await target.reply_text("Belum ada data transaksi untuk ditampilkan dalam grafik.")
        return

    dates = [datetime.strptime(row[0], "%Y-%m-%d") for row in data]
    pemasukan = [row[1] for row in data]
    pengeluaran = [row[2] for row in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, pemasukan, label="Pemasukan", color="green", marker="o")
    plt.plot(dates, pengeluaran, label="Pengeluaran", color="red", marker="o")
    plt.title("Grafik Keuangan")
    plt.xlabel("Tanggal")
    plt.ylabel("Jumlah (Rp)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    target = update.message or update.callback_query.message
    await target.chat.send_action(action=ChatAction.UPLOAD_PHOTO)
    await target.reply_photo(photo=buffer)

grafik_cmd = CommandHandler("grafik", grafik)

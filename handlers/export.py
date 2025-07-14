import sqlite3
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes
from io import BytesIO

async def export_excel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect("keuangan.db")
    c = conn.cursor()

    try:
        c.execute("""
            SELECT type, amount, source, description, kategori, timestamp
            FROM transactions
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """, (user_id,))
    except sqlite3.OperationalError as e:
        await (update.message or update.callback_query.message).reply_text(
            f"⚠️ Error saat mengambil data: {e}"
        )
        return

    rows = c.fetchall()
    conn.close()

    if not rows:
        await (update.message or update.callback_query.message).reply_text("Tidak ada data transaksi untuk diexport.")
        return

    df = pd.DataFrame(rows, columns=["Tipe", "Jumlah", "Sumber", "Deskripsi", "Kategori", "Tanggal"])
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Transaksi', index=False)
    buffer.seek(0)

    await (update.message or update.callback_query.message).reply_document(
        document=buffer,
        filename="transaksi_keuangan.xlsx",
        caption="📁 Berikut data transaksi kamu dalam format Excel."
    )

from telegram.ext import CommandHandler
export_cmd = CommandHandler("export", export_excel)

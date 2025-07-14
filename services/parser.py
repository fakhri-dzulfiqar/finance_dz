import re
import sqlite3
from datetime import datetime
from model.kategori import KATEGORI_PEMASUKAN

def parse_transaction(user_id: str, text: str) -> str:
    hasil = []
    baris_list = text.strip().split('\n')

    conn = sqlite3.connect("keuangan.db")
    c = conn.cursor()

    for baris in baris_list:
        baris = baris.strip()
        if not baris:
            continue

        match = re.match(r"^(\d{1,2} \w+)\s+(\d{3,}|\d+[.,]?\d*)\s+(.+)$", baris)
        if not match:
            continue

        tanggal_str, jumlah_str, keterangan = match.groups()
        jumlah = int(str(jumlah_str).replace('.', '').replace(',', ''))

        # Konversi tanggal
        try:
            tanggal = datetime.strptime(tanggal_str + " " + str(datetime.now().year), "%d %B %Y")
        except ValueError:
            continue

        tipe = 'masuk' if any(keyword.lower() in keterangan.lower() for keyword in KATEGORI_PEMASUKAN) else 'keluar'

        # Simpan ke DB
        c.execute("""
            INSERT INTO transactions (user_id, amount, type, description, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, jumlah, tipe, keterangan.strip(), tanggal.isoformat()))

        hasil.append(f"✅ {jumlah:,} ({tipe.title()}): {keterangan.strip()}")

    conn.commit()
    conn.close()

    if not hasil:
        return "⚠️ Tidak ada transaksi valid yang dikenali."
    return "\n".join(hasil)

# --- File: services/database.py ---
import sqlite3
from datetime import datetime
from model.kategori import KATEGORI_MAP

conn = sqlite3.connect('keuangan.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        type TEXT CHECK(type IN ('masuk', 'keluar')),
        amount INTEGER,
        source TEXT,
        description TEXT,
        kategori TEXT DEFAULT 'Lainnya',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

def insert_transaction(user_id, type_, amount, description, source='Unknown', timestamp=None):
    if not timestamp:
        timestamp = datetime.now()

    kategori = 'Lainnya'
    for keyword, kat in KATEGORI_MAP.items():
        if keyword in description.lower():
            kategori = kat
            break

    c.execute("""
        INSERT INTO transactions (user_id, type, amount, source, description, kategori, timestamp) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (user_id, type_, amount, source, description, kategori, timestamp))
    conn.commit()

def get_summary(user_id):
    now = datetime.now()
    start = datetime(now.year, now.month, 10)
    end = datetime(now.year if now.month < 12 else now.year + 1, (now.month % 12) + 1, 10)
    c.execute("""
        SELECT type, source, SUM(amount)
        FROM transactions
        WHERE user_id = ? AND timestamp BETWEEN ? AND ?
        GROUP BY type, source
    """, (user_id, start, end))
    rows = c.fetchall()
    data = {'masuk': {}, 'keluar': {}}
    for row in rows:
        data[row[0]][row[1]] = row[2]
    return data

def get_summary_message(user_id):
    data = get_summary(user_id)
    masuk_total = sum(data['masuk'].values())
    keluar_total = sum(data['keluar'].values())
    saldo_total = masuk_total - keluar_total
    lines = [
        "📊 *Statistik Keuangan Bulan Ini*",
        f"🟢 Total Pemasukan : Rp{masuk_total:,.0f}".replace(",", "."),
    ]
    for src, amt in data['masuk'].items():
        lines.append(f"   └ {src}: Rp{amt:,.0f}".replace(",", "."))
    lines.append(f"🔴 Total Pengeluaran : Rp{keluar_total:,.0f}".replace(",", "."))
    for src, amt in data['keluar'].items():
        lines.append(f"   └ {src}: Rp{amt:,.0f}".replace(",", "."))
    lines.append(f"💰 *Saldo Bersih* : Rp{saldo_total:,.0f}".replace(",", "."))
    return "\n".join(lines)

def get_all_transactions(user_id):
    c.execute("""
        SELECT type, amount, source, description, kategori, timestamp 
        FROM transactions WHERE user_id = ? ORDER BY timestamp DESC
    """, (user_id,))
    return c.fetchall()
# --- File: services/chart.py ---
import matplotlib.pyplot as plt
from datetime import datetime
from services.database import conn, c

def generate_chart(user_id):
    now = datetime.now()
    start = datetime(now.year, now.month, 1)
    end = datetime(now.year if now.month < 12 else now.year + 1, (now.month % 12) + 1, 1)
    c.execute("""
        SELECT type, date(timestamp), SUM(amount) 
        FROM transactions 
        WHERE user_id = ? AND timestamp BETWEEN ? AND ?
        GROUP BY type, date(timestamp)
        ORDER BY date(timestamp)
    """, (user_id, start, end))
    rows = c.fetchall()
    if not rows:
        return None
    data = {}
    for t, d, a in rows:
        data.setdefault(d, {'masuk': 0, 'keluar': 0})
        data[d][t] += a
    dates = sorted(data.keys())
    pemasukan = [data[d]['masuk'] for d in dates]
    pengeluaran = [data[d]['keluar'] for d in dates]
    plt.figure(figsize=(10, 5))
    plt.bar(dates, pemasukan, label="Pemasukan", color="green")
    plt.bar(dates, pengeluaran, bottom=pemasukan, label="Pengeluaran", color="red")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    filename = f"chart_{user_id}.png"
    plt.savefig(filename)
    plt.close()
    return filename

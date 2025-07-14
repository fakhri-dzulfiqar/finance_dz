# --- File: services/parser.py ---
import re
from datetime import datetime
from services.database import insert_transaction, get_summary_message

def parse_amount(text):
    return int(text.replace('.', '').replace(',', '').strip())

def parse_transaction(user_id, text):
    if text.lower().startswith("pemasukan"):
        match = re.match(r"Pemasukan\s+([\d\.,]+)\s+(.+?)(?:\s+via\s+(\w+))?$", text, re.IGNORECASE)
        if match:
            amount = parse_amount(match.group(1))
            desc = match.group(2)
            source = match.group(3) or "Unknown"
            insert_transaction(user_id, 'masuk', amount, desc, source)
            return f"✅ Pemasukan *Rp{amount:,}* dari *{source}* dicatat:\n_{desc}_\n\n" + get_summary_message(user_id)
        return "Format salah. Contoh: `Pemasukan 1.000.000 Gaji via BRI`"

    match = re.match(r"(\d{1,2})\s*(\w+)?\s+([\d\.,]+)\s+(.+?)(?:\s+dari\s+(\w+))?$", text, re.IGNORECASE)
    if match:
        day = int(match.group(1))
        month_text = match.group(2)
        amount = parse_amount(match.group(3))
        desc = match.group(4)
        source = match.group(5) or "Unknown"
        try:
            if month_text:
                date = datetime.strptime(f"{day} {month_text}", "%d %B").replace(year=datetime.now().year)
            else:
                date = datetime.now().replace(day=day)
        except:
            date = datetime.now()
        insert_transaction(user_id, 'keluar', amount, desc, source, date)
        return f"❌ Pengeluaran *Rp{amount:,}* dari *{source}* dicatat:\n_{desc}_\n\n" + get_summary_message(user_id)

    return "📝 Format tidak dikenali.\nContoh:\n`Pemasukan 1.000.000 Gaji via BCA`\n`14 Juli 10.000 Parkir dari Cash`"

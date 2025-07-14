import re
from datetime import datetime
from model.kategori import KATEGORI_PEMASUKAN

def parse_transaksi(text):
    hasil = []
    baris_list = text.strip().split('\n')
    
    for baris in baris_list:
        baris = baris.strip()
        if not baris:
            continue

        # Cocokkan format seperti: "14 Juli 123456 Keterangan"
        match = re.match(r"^(\d{1,2} \w+)\s+(\d{3,}|\d+[.,]?\d*)\s+(.+)$", baris)
        if not match:
            continue

        tanggal, jumlah, keterangan = match.groups()

        # Bersihkan jumlah dari titik/koma
        jumlah = int(str(jumlah).replace('.', '').replace(',', ''))

        # Deteksi apakah termasuk pemasukan atau pengeluaran
        if any(keyword.lower() in keterangan.lower() for keyword in KATEGORI_PEMASUKAN):
            kategori = "Pemasukan"
        else:
            kategori = "Pengeluaran"

        hasil.append({
            "tanggal": tanggal,
            "kategori": kategori,
            "jumlah": jumlah,
            "keterangan": keterangan.strip()
        })

    return hasil

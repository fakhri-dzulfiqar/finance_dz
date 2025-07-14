import re
from datetime import datetime
from model.kategori import KATEGORI_PEMASUKAN, KATEGORI_PENGELUARAN

def parse_transaksi(text):
    hasil = []
    baris_list = text.strip().split('\n')
    tanggal_sekarang = datetime.now().strftime("%d %B")

    for baris in baris_list:
        baris = baris.strip()
        if not baris:
            continue

        # Format lengkap: "14 Juli 100000 Parkir dari Cash"
        match = re.match(r"^(\d{1,2} \w+) (\d+[.,]?\d*) (.+)", baris)
        if match:
            tanggal, jumlah, keterangan = match.groups()
        else:
            # Format tanpa tanggal: "100000 Parkir dari Cash"
            match2 = re.match(r"^(\d+[.,]?\d*) (.+)", baris)
            if match2:
                tanggal = tanggal_sekarang
                jumlah, keterangan = match2.groups()
            else:
                # Format terbalik: "Parkir dari Cash 100000"
                match3 = re.match(r"^(.+) (\d+[.,]?\d*)$", baris)
                if match3:
                    keterangan, jumlah = match3.groups()
                    tanggal = tanggal_sekarang
                else:
                    # Tidak dikenali
                    continue

        jumlah = int(str(jumlah).replace('.', '').replace(',', ''))

        # Deteksi otomatis jenis berdasarkan kata kunci
        lower_ket = keterangan.lower()
        if any(kw in lower_ket for kw in KATEGORI_PEMASUKAN):
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

"""
File: dummy_data.py
Deskripsi: Menghasilkan data simulasi secara otomatis agar memenuhi syarat 100+ data.
"""

import random
from models import Penerima, Bantuan, Posko

def generate_dummy_penerima(jumlah=100):
    """Menghasilkan sekumpulan data penerima bantuan secara acak"""
    daftar_penerima = []
    
    nama_depan = ["Budi", "Siti", "Andi", "Eko", "Hadi", "Sri", "Joko", "Ayu", "Putra", "Dewi", "Agus", "Rina", "Iwan", "Sari", "Nina"]
    nama_belakang = ["Saputra", "Wulandari", "Setiawan", "Lestari", "Hidayat", "Rahmawati", "Kurniawan", "Ningsih", "Pratama", "Wijaya"]
    desa = ["Desa Sukamaju", "Desa Harapan", "Desa Makmur", "Desa Sejahtera", "Desa Sukaasih", "Desa Karanganyar", "Desa Pringgodani"]

    for i in range(1, jumlah + 1):
        # Format ID: P001, P002, ..., P100
        id_p = f"P{str(i).zfill(3)}" 
        nama = f"{random.choice(nama_depan)} {random.choice(nama_belakang)}"
        jml_keluarga = random.randint(1, 8)
        lokasi = random.choice(desa)
        
        penerima = Penerima(id_p, nama, jml_keluarga, lokasi)
        daftar_penerima.append(penerima)
        
    return daftar_penerima

def generate_dummy_bantuan():
    """Menghasilkan data master logistik dengan stok tinggi"""
    return [
        Bantuan("B01", "Sembako Lengkap", 500, "Paket"),
        Bantuan("B02", "Obat-obatan P3K", 200, "Kotak"),
        Bantuan("B03", "Air Mineral", 1000, "Kardus"),
        Bantuan("B04", "Tenda Darurat", 50, "Unit"),
        Bantuan("B05", "Pakaian Layak Pakai", 300, "Karung")
    ]

def generate_dummy_posko():
    """Menghasilkan data posko untuk dipetakan ke dalam Graph"""
    return [
        Posko("PSK-01", "Posko Utama Terpadu", "Kecamatan Pusat"),
        Posko("PSK-02", "Posko Darurat Utara", "Kecamatan Utara"),
        Posko("PSK-03", "Posko Darurat Selatan", "Kecamatan Selatan"),
        Posko("PSK-04", "Posko Medis Timur", "Kecamatan Timur")
    ]
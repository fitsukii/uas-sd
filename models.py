"""
File: models.py
Deskripsi: Berisi blueprint (cetak biru) untuk entitas data dalam sistem.
"""

class Penerima:
    def __init__(self, id_penerima, nama, jml_keluarga, lokasi):
        self.id_penerima = id_penerima
        self.nama = nama
        self.jml_keluarga = jml_keluarga
        self.lokasi = lokasi

    def __str__(self):
        # Format tampilan saat di-print
        return f"[{self.id_penerima}] {self.nama} | Keluarga: {self.jml_keluarga} Jiwa | Lokasi: {self.lokasi}"


class Bantuan:
    def __init__(self, id_bantuan, jenis, jumlah, satuan):
        self.id_bantuan = id_bantuan
        self.jenis = jenis
        self.jumlah = jumlah
        self.satuan = satuan

    def kurangi_stok(self, jml_diambil):
        """Mengurangi stok saat bantuan didistribusikan"""
        if self.jumlah >= jml_diambil:
            self.jumlah -= jml_diambil
            return True
        return False

    def tambah_stok(self, jml_dikembalikan):
        """Menambah stok saat distribusi dibatalkan (undo)"""
        self.jumlah += jml_dikembalikan

    def __str__(self):
        return f"[{self.id_bantuan}] {self.jenis} | Stok: {self.jumlah} {self.satuan}"


class Distribusi:
    def __init__(self, id_distribusi, id_penerima, id_bantuan, tanggal, status="Selesai"):
        self.id_distribusi = id_distribusi
        self.id_penerima = id_penerima
        self.id_bantuan = id_bantuan
        self.tanggal = tanggal
        self.status = status

    def batalkan(self):
        """Mengubah status jika distribusi dibatalkan melalui Stack (Undo)"""
        self.status = "Dibatalkan"

    def __str__(self):
        return (f"Distribusi {self.id_distribusi} | Tgl: {self.tanggal} | "
                f"Penerima: {self.id_penerima} | Bantuan: {self.id_bantuan} | Status: {self.status}")


class Posko:
    def __init__(self, id_posko, nama_posko, lokasi):
        self.id_posko = id_posko
        self.nama_posko = nama_posko
        self.lokasi = lokasi

    def __str__(self):
        return f"[{self.id_posko}] {self.nama_posko} - {self.lokasi}"
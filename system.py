"""
File: system.py
Deskripsi: Otak utama aplikasi. Menyatukan entitas, struktur data, dan interaksi pengguna.
"""

from structures import ArrayList, LinkedList, Stack, Queue, BST, HashTable, Graph
from models import Distribusi
from dummy_data import generate_dummy_penerima, generate_dummy_bantuan, generate_dummy_posko
import datetime

class SistemBencana:
    def __init__(self):
        # 1. Inisialisasi semua struktur data
        self.list_penerima = ArrayList()
        self.list_bantuan = ArrayList()
        
        self.antrean_penerima = Queue()
        self.riwayat_distribusi = LinkedList()
        self.stack_undo = Stack()
        
        self.bst_penerima = BST()
        self.hash_bantuan = HashTable(size=10)
        self.graph_posko = Graph()
        
        self.id_distribusi_counter = 1

        # 2. Muat data dummy secara otomatis
        self.load_data_awal()

    def load_data_awal(self):
        print("[SISTEM] Memuat data simulasi...")
        
        # Load Penerima
        for p in generate_dummy_penerima(100):
            self.list_penerima.insert(p)                  # Masuk Array (Data Master)
            self.bst_penerima.insert(p.id_penerima, p)    # Masuk BST (Untuk pencarian)
            self.antrean_penerima.enqueue(p)              # Masuk Antrean (Queue)
            
        # Load Bantuan
        for b in generate_dummy_bantuan():
            self.list_bantuan.insert(b)                   # Masuk Array
            self.hash_bantuan.insert(b.id_bantuan, b)     # Masuk Hash Table (Pencarian cepat)
            
        # Load Posko ke Graph
        posko_data = generate_dummy_posko()
        for posko in posko_data:
            self.graph_posko.add_vertex(posko.nama_posko)
            
        # Buat jalur antar posko (Edge)
        self.graph_posko.add_edge("Posko Utama Terpadu", "Posko Darurat Utara")
        self.graph_posko.add_edge("Posko Utama Terpadu", "Posko Darurat Selatan")
        self.graph_posko.add_edge("Posko Darurat Utara", "Posko Medis Timur")
        
        print("[SISTEM] 100 Data Penerima, 5 Bantuan, dan Peta Posko berhasil dimuat!\n")

    # ==========================================
    # FITUR-FITUR APLIKASI
    # ==========================================
    def lihat_antrean(self):
        if self.antrean_penerima.is_empty():
            print("\n>> Tidak ada antrean saat ini.")
        else:
            penerima_depan = self.antrean_penerima.front()
            print(f"\n>> Antrean terdepan saat ini: {penerima_depan.nama} ({penerima_depan.id_penerima})")

    def proses_distribusi(self):
        if self.antrean_penerima.is_empty():
            print("\n>> Antrean kosong. Tidak ada penerima yang menunggu.")
            return

        # Ambil korban dari antrean terdepan (Dequeue)
        penerima = self.antrean_penerima.dequeue()
        print(f"\n--- PROSES PENYALURAN BANTUAN ---")
        print(f"Penerima : {penerima.nama} ({penerima.id_penerima}) - {penerima.lokasi}")
        print("Daftar Bantuan Tersedia:")
        
        for b in self.list_bantuan.get_all():
            print(b)
            
        id_bantuan = input("Masukkan ID Bantuan yang diberikan (Contoh: B01): ").upper()
        
        # Cari bantuan menggunakan Hash Table (O(1))
        bantuan = self.hash_bantuan.search(id_bantuan)
        
        if bantuan:
            try:
                jml_diambil = int(input(f"Jumlah {bantuan.satuan} yang diberikan: "))
                # Kurangi stok
                if bantuan.kurangi_stok(jml_diambil):
                    tgl_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    id_dist = f"DST-{self.id_distribusi_counter:03d}"
                    self.id_distribusi_counter += 1
                    
                    # Buat objek Distribusi
                    distribusi_baru = Distribusi(id_dist, penerima.id_penerima, bantuan.id_bantuan, tgl_sekarang)
                    
                    # Simpan ke Riwayat (Linked List) dan Stack (Undo)
                    self.riwayat_distribusi.insert_last(distribusi_baru)
                    self.stack_undo.push(distribusi_baru)
                    self.stack_undo.push(jml_diambil) # Simpan jumlah juga untuk undo stok
                    
                    print(f"\n>> BERHASIL! Bantuan disalurkan kepada {penerima.nama}.")
                else:
                    print("\n>> GAGAL! Stok bantuan tidak mencukupi.")
            except ValueError:
                print("\n>> GAGAL! Jumlah harus berupa angka.")
        else:
            print("\n>> GAGAL! ID Bantuan tidak ditemukan.")

    def batalkan_distribusi(self):
        if self.stack_undo.is_empty():
            print("\n>> Tidak ada riwayat distribusi yang bisa dibatalkan.")
            return
            
        # Ambil data dari Stack (Pop)
        jml_dikembalikan = self.stack_undo.pop()
        distribusi_batal = self.stack_undo.pop()
        
        # Hapus riwayat terakhir dari Linked List
        self.riwayat_distribusi.delete_last()
        
        # Kembalikan stok bantuan
        bantuan = self.hash_bantuan.search(distribusi_batal.id_bantuan)
        if bantuan:
            bantuan.tambah_stok(jml_dikembalikan)
            
        # Ubah status
        distribusi_batal.batalkan()
        
        print(f"\n>> UNDO BERHASIL! Distribusi {distribusi_batal.id_distribusi} dibatalkan.")
        print(f">> {jml_dikembalikan} stok dikembalikan ke {bantuan.jenis}.")

    def cari_penerima(self):
        id_cari = input("\nMasukkan ID Penerima (Contoh: P005): ").upper()
        # Menggunakan BST untuk pencarian cepat (O(log N))
        hasil = self.bst_penerima.search(id_cari)
        if hasil:
            print("\n>> Data Ditemukan:")
            print(hasil.data)
        else:
            print("\n>> Data tidak ditemukan.")

    def lihat_riwayat(self):
        print("\n--- RIWAYAT DISTRIBUSI (LINKED LIST) ---")
        riwayat = self.riwayat_distribusi.traverse()
        if not riwayat:
            print("Belum ada riwayat distribusi.")
        else:
            for r in riwayat:
                print(r)

    def lihat_jaringan_posko(self):
        print("\n--- JARINGAN POSKO (GRAPH BFS) ---")
        jalur = self.graph_posko.bfs("Posko Utama Terpadu")
        print(" -> ".join(jalur))

    # ==========================================
    # MENU CLI
    # ==========================================
    def jalankan_menu(self):
        while True:
            print("\n" + "="*45)
            print(" SISTEM PENANGGULANGAN BENCANA (KELOMPOK 7) ")
            print("="*45)
            print("1. Panggil Antrean & Salurkan Bantuan (Queue, Hash)")
            print("2. Batalkan Distribusi Terakhir (Stack Undo)")
            print("3. Lihat Riwayat Distribusi (Linked List)")
            print("4. Cari Data Penerima Bantuan (BST)")
            print("5. Lihat Sisa Stok Bantuan (Array/Hash)")
            print("6. Lihat Jaringan Posko (Graph BFS)")
            print("7. Lihat Antrean Terdepan")
            print("0. Keluar")
            print("="*45)
            
            pilihan = input("Pilih menu (0-7): ")
            
            if pilihan == '1':
                self.proses_distribusi()
            elif pilihan == '2':
                self.batalkan_distribusi()
            elif pilihan == '3':
                self.lihat_riwayat()
            elif pilihan == '4':
                self.cari_penerima()
            elif pilihan == '5':
                print("\n--- SISA STOK BANTUAN ---")
                for b in self.list_bantuan.get_all():
                    print(b)
            elif pilihan == '6':
                self.lihat_jaringan_posko()
            elif pilihan == '7':
                self.lihat_antrean()
            elif pilihan == '0':
                print("\nTerima kasih telah menggunakan sistem ini. Tetap semangat!\n")
                break
            else:
                print("\nPilihan tidak valid. Silakan coba lagi.")
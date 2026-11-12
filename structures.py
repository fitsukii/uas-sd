"""
File: structures.py
Deskripsi: Berisi implementasi seluruh struktur data yang dibutuhkan sesuai ADT.
"""

# ==========================================
# 1. ARRAY / LIST 
# Digunakan untuk Data Penerima & Bantuan
# ==========================================
class ArrayList:
    def __init__(self):
        # Menggunakan list Python sebagai media penyimpanan dasar
        self.items = []

    def insert(self, data):
        """Menambahkan data ke bagian akhir array"""
        self.items.append(data)

    def delete(self, id_data, key_attr):
        """
        Menghapus objek berdasarkan ID.
        key_attr adalah nama atribut ID pada objek (misal: 'id_penerima')
        """
        for i in range(len(self.items)):
            # Menggunakan getattr untuk mengambil nilai atribut objek secara dinamis
            if getattr(self.items[i], key_attr) == id_data:
                del self.items[i]
                return True
        return False

    def search(self, id_data, key_attr):
        """Mencari objek berdasarkan ID (Linear Search)"""
        for item in self.items:
            if getattr(item, key_attr) == id_data:
                return item
        return None

    def get_all(self):
        """Mengembalikan seluruh isi array"""
        return self.items


# ==========================================
# 2. LINKED LIST (Single Linked List)
# Digunakan untuk Riwayat Distribusi Bantuan
# ==========================================
class Node:
    def __init__(self, data):
        self.data = data  # Menyimpan objek Distribusi
        self.next = None  # Pointer ke node berikutnya

class LinkedList:
    def __init__(self):
        self.head = None  # Menunjuk ke node pertama (riwayat terlama)
        self.tail = None  # Menunjuk ke node terakhir (riwayat terbaru)

    def insert_last(self, data):
        """Menambahkan riwayat distribusi baru di akhir rantai"""
        new_node = Node(data)
        if self.head is None:
            # Jika masih kosong, head dan tail menunjuk ke node yang sama
            self.head = new_node
            self.tail = new_node
        else:
            # Sambungkan tail lama ke node baru
            self.tail.next = new_node
            # Pindahkan status tail ke node baru
            self.tail = new_node

    def delete_last(self):
        """
        Menghapus riwayat distribusi terakhir (membatalkan distribusi).
        Mengembalikan data yang dihapus, atau None jika kosong.
        """
        if self.head is None:
            return None # List kosong
        
        # Jika hanya ada 1 node
        if self.head.next is None:
            deleted_data = self.head.data
            self.head = None
            self.tail = None
            return deleted_data

        # Jika node lebih dari 1, cari node SEBELUM tail
        current = self.head
        while current.next != self.tail:
            current = current.next
        
        deleted_data = self.tail.data
        # Putuskan rantai
        current.next = None
        self.tail = current
        return deleted_data

    def traverse(self):
        """Menelusuri dan mengembalikan list berisi semua data dari head ke tail"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result
    
# ==========================================
# 3. STACK
# Digunakan untuk riwayat koreksi/pembatalan (Undo) (LIFO)
# ==========================================
class Stack:
    def __init__(self):
        self.items = []

    def push(self, data):
        """Menambahkan data ke tumpukan paling atas"""
        self.items.append(data)

    def pop(self):
        """Mengambil dan menghapus data dari tumpukan paling atas (LIFO)"""
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        """Melihat data teratas tanpa menghapusnya"""
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        """Mengecek apakah stack kosong"""
        return len(self.items) == 0


# ==========================================
# 4. QUEUE
# Digunakan untuk antrean penerima bantuan (FIFO)
# ==========================================
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, data):
        """Memasukkan data ke antrean paling belakang"""
        self.items.append(data)

    def dequeue(self):
        """Mengambil dan menghapus data dari antrean paling depan (FIFO)"""
        if not self.is_empty():
            return self.items.pop(0) # Mengambil indeks ke-0
        return None

    def front(self):
        """Melihat data paling depan tanpa menghapusnya"""
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        """Mengecek apakah antrean kosong"""
        return len(self.items) == 0

# ==========================================
# 5. BINARY SEARCH TREE (BST)
# Digunakan untuk pencarian cepat data Penerima berdasarkan ID
# ==========================================
class NodeBST:
    def __init__(self, key_id, data):
        self.key_id = key_id  # String ID sebagai kunci pengurutan (misal: "P01")
        self.data = data      # Objek Penerima
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    # --- INSERT ---
    def insert(self, key_id, data):
        if self.root is None:
            self.root = NodeBST(key_id, data)
        else:
            self._insert_recursive(self.root, key_id, data)

    def _insert_recursive(self, node, key_id, data):
        # Membandingkan string secara alfabetis
        if key_id < node.key_id:
            if node.left is None:
                node.left = NodeBST(key_id, data)
            else:
                self._insert_recursive(node.left, key_id, data)
        elif key_id > node.key_id:
            if node.right is None:
                node.right = NodeBST(key_id, data)
            else:
                self._insert_recursive(node.right, key_id, data)
        # Jika sama (duplikat), kita abaikan (tidak dimasukkan)

    # --- SEARCH ---
    def search(self, key_id):
        return self._search_recursive(self.root, key_id)

    def _search_recursive(self, node, key_id):
        # Base case: root null atau key ada di node
        if node is None or node.key_id == key_id:
            return node
        
        # Key lebih besar dari key node saat ini
        if node.key_id < key_id:
            return self._search_recursive(node.right, key_id)
        
        # Key lebih kecil dari key node saat ini
        return self._search_recursive(node.left, key_id)

    # --- DELETE ---
    def delete(self, key_id):
        self.root = self._delete_recursive(self.root, key_id)

    def _delete_recursive(self, root, key_id):
        if root is None:
            return root

        # Cari node yang akan dihapus
        if key_id < root.key_id:
            root.left = self._delete_recursive(root.left, key_id)
        elif key_id > root.key_id:
            root.right = self._delete_recursive(root.right, key_id)
        else:
            # Node dengan satu anak atau tanpa anak
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            # Node dengan dua anak: Dapatkan penerus inorder (terkecil di subpohon kanan)
            temp = self._min_value_node(root.right)
            # Salin konten penerus inorder ke node ini
            root.key_id = temp.key_id
            root.data = temp.data
            # Hapus penerus inorder
            root.right = self._delete_recursive(root.right, temp.key_id)

        return root

    def _min_value_node(self, node):
        current = node
        # Loop ke bawah untuk menemukan daun paling kiri
        while(current.left is not None):
            current = current.left
        return current

    # --- TRAVERSAL ---
    def preorder(self):
        """Root -> Left -> Right"""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, root, result):
        if root:
            result.append(root.key_id)
            self._preorder_recursive(root.left, result)
            self._preorder_recursive(root.right, result)

    def inorder(self):
        """Left -> Root -> Right (Menghasilkan data terurut)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, root, result):
        if root:
            self._inorder_recursive(root.left, result)
            result.append(root.key_id)
            self._inorder_recursive(root.right, result)

    def postorder(self):
        """Left -> Right -> Root"""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, root, result):
        if root:
            self._postorder_recursive(root.left, result)
            self._postorder_recursive(root.right, result)
            result.append(root.key_id)
            
# ==========================================
# 6. HASH TABLE
# Digunakan untuk pencarian instan Data Bantuan Logistik
# ==========================================
class HashTable:
    def __init__(self, size=10):
        self.size = size
        # Menggunakan metode Chaining (List of Lists) untuk mengatasi collision
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key_id):
        """Hash function sederhana: jumlahkan nilai ASCII string lalu di-modulo"""
        return sum(ord(char) for char in key_id) % self.size

    def insert(self, key_id, data):
        index = self._hash(key_id)
        # Jika key sudah ada, update datanya
        for i, kv in enumerate(self.table[index]):
            if kv[0] == key_id:
                self.table[index][i] = (key_id, data)
                return
        # Jika belum ada, tambahkan ke dalam chain (list pada indeks tersebut)
        self.table[index].append((key_id, data))

    def search(self, key_id):
        index = self._hash(key_id)
        for kv in self.table[index]:
            if kv[0] == key_id:
                return kv[1] # Mengembalikan data objeknya
        return None

    def delete(self, key_id):
        index = self._hash(key_id)
        for i, kv in enumerate(self.table[index]):
            if kv[0] == key_id:
                del self.table[index][i]
                return True
        return False


# ==========================================
# 7. GRAPH (Undirected & Unweighted)
# Digunakan untuk memetakan jaringan rute antar-Posko
# ==========================================
class Graph:
    def __init__(self):
        # Menggunakan Adjacency List (Dictionary)
        self.adj_list = {}

    def add_vertex(self, vertex_id):
        """Menambahkan posko baru (titik) ke dalam peta"""
        if vertex_id not in self.adj_list:
            self.adj_list[vertex_id] = []

    def add_edge(self, v1, v2):
        """Menghubungkan dua posko dengan jalur (dua arah/undirected)"""
        # Pastikan kedua vertex ada
        if v1 in self.adj_list and v2 in self.adj_list:
            if v2 not in self.adj_list[v1]:
                self.adj_list[v1].append(v2)
            if v1 not in self.adj_list[v2]:
                self.adj_list[v2].append(v1)

    def bfs(self, start_vertex):
        """Breadth-First Search: Menelusuri posko terdekat lebih dulu"""
        if start_vertex not in self.adj_list:
            return []
            
        visited = set()
        queue = [start_vertex]
        visited.add(start_vertex)
        result = []
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            
            for neighbor in self.adj_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result

    def dfs(self, start_vertex):
        """Depth-First Search: Menelusuri jalur posko sedalam-dalamnya"""
        if start_vertex not in self.adj_list:
            return []
            
        visited = set()
        result = []
        self._dfs_recursive(start_vertex, visited, result)
        return result

    def _dfs_recursive(self, vertex, visited, result):
        visited.add(vertex)
        result.append(vertex)
        
        for neighbor in self.adj_list[vertex]:
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, result)
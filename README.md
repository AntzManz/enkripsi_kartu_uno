# 🔒 UNO Encryption Tools (Web Version)

UNO Encryption Tools adalah aplikasi web modern (Single Page Application) untuk simulasi enkripsi pesan menggunakan algoritma kustom yang dinamakan UnoCipher.

Proyek ini merupakan porting dari versi Python/Streamlit ke React.js, yang memungkinkan aplikasi berjalan sepenuhnya di sisi klien (browser) dengan performa tinggi dan antarmuka yang responsif. Data riwayat enkripsi disimpan secara persisten menggunakan LocalStorage browser.



## ✨ Fitur Utama

#### 1. 🏠 Halaman User (Enkripsi)

Algoritma UnoCipher: Logika enkripsi unik menggunakan grid karakter 3 baris dengan Key Offset dinamis.

Enkripsi Instan: Cukup masukkan Key, Shift, dan Plain Text untuk mendapatkan kode rahasia.

Auto-History: Hasil enkripsi otomatis tersimpan ke memori lokal browser tanpa perlu login.



#### 2. ⚙️ Halaman Admin (Dashboard)

Secure Access: Area admin terlindungi password sederhana (Default: admin123).

Manajemen Data (CRUD):

Read: Monitoring tabel riwayat enkripsi.

Update: Koreksi data input (Input Text, Key, Shift) dengan kalkulasi ulang otomatis.

Delete: Hapus data per baris.

Reset DB: Hapus total seluruh database lokal.



#### 3. 💾 Client-Side Storage

Tanpa Database Server: Menggunakan API LocalStorage browser.

Persisten: Data tetap ada meskipun browser ditutup atau di-refresh.

Privasi: Data tersimpan eksklusif di perangkat pengguna.

---

### 🛠️ Tech Stack

Frontend Framework: React.js (Vite)

Styling: Tailwind CSS

Icons: Lucide React

Storage: Browser LocalStorage API

---

### 📖 Logika Algoritma (UnoCipher)

Algoritma ini bekerja dengan langkah berikut:

Generate Grid: Membuat tabel referensi 3 baris x 10 kolom. Header kolom digenerate berdasarkan Key yang dimasukkan user.

Find Position: Mencari koordinat (baris & kolom) dari setiap huruf pada Plain Text.

Shift Operation: Menggeser posisi kolom sejauh nilai Shift Pattern.

Encoding: Mengambil karakter dari header kolom baru sebagai Cipher Text.

---

### 🔐 Akun Admin Default

Untuk mengakses halaman admin dashboard:

Password: admin123

(Anda dapat mengubah password ini di file App.jsx pada bagian handleLogin)

---

### 🤝 Kontribusi

Kontribusi sangat terbuka! Jika Anda ingin memperbaiki bug atau menambahkan fitur:

Fork repository ini.

Buat branch fitur baru (git checkout -b fitur-baru).

Commit perubahan Anda (git commit -m 'Menambahkan fitur baru').

Push ke branch (git push origin fitur-baru).

Buat Pull Request.

---

### 👨‍💻 Author

Dibuat dengan ❤️ oleh Ananta Ramadhani

NIM: 24.83.1062

Institusi: Universitas AMIKOM Yogyakarta

Catatan: Aplikasi ini menggunakan LocalStorage. Membersihkan cache browser akan menghapus riwayat data enkripsi.

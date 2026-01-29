import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="UNO Encryption Tools", page_icon="🔒", layout="centered")

# --- BAGIAN 1: LOGIKA ENKRIPSI (OOP) ---
class UnoCipher:
    def __init__(self):
        self.row_chars = [
            ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            ["K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
            ["U", "V", "W", "X", "Y", "Z", "1", "2", "3", "4"]
        ]
        self.row_key_offsets = [0, 4, 2]

    def _generate_grid(self, key_str):
        grid = []
        key_arr = list(key_str)
        # Handle jika key lebih pendek dari kebutuhan (looping key)
        if len(key_arr) == 0: return []
        
        for r in range(3):
            headers = []
            start_idx = self.row_key_offsets[r]
            for c in range(10):
                key_char = key_arr[(start_idx + c) % len(key_arr)]
                num = (c + 1) % 10
                headers.append(f"{key_char}{num}")
            grid.append({"headers": headers, "chars": self.row_chars[r]})
        return grid

    def _find_char(self, grid, char):
        char = char.upper()
        for r in range(len(grid)):
            if char in grid[r]["chars"]:
                return {"row": r, "col": grid[r]["chars"].index(char)}
        return None

    def encrypt(self, text, key, shift):
        text = text.upper().replace(" ", "")
        key = key.upper()
        
        if not key or not shift: return "Error: Key/Shift kosong"
        
        shifts = [int(x) for x in str(shift) if x.isdigit()]
        if not shifts: return "Error: Pola Shift harus angka"
        
        grid = self._generate_grid(key)
        if not grid: return "Error: Gagal generate grid"

        output = []
        shift_idx = 0
        
        for char in text:
            pos = self._find_char(grid, char)
            if pos:
                s = shifts[shift_idx % len(shifts)]
                new_col = (pos["col"] + s) % 10
                code = grid[pos["row"]]["headers"][new_col]
                output.append(code)
                shift_idx += 1
        return "".join(output)

# --- BAGIAN 2: MANAJEMEN DATABASE (CRUD) ---
DB_NAME = 'uno_history.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            input_text TEXT,
            key_code TEXT,
            shift_pattern TEXT,
            result_text TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Create
def save_to_db(text, key, shift, result):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO history (timestamp, input_text, key_code, shift_pattern, result_text) VALUES (?,?,?,?,?)',
              (timestamp, text, key, shift, result))
    conn.commit()
    conn.close()

# Read
def load_history():
    if not os.path.exists(DB_NAME):
        init_db()
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
    conn.close()
    return df

# Update
def update_data(id_data, text, key, shift, result):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE history 
        SET input_text=?, key_code=?, shift_pattern=?, result_text=?
        WHERE id=?
    ''', (text, key, shift, result, id_data))
    conn.commit()
    conn.close()

# Delete (Single)
def delete_data(id_data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM history WHERE id=?', (id_data,))
    conn.commit()
    conn.close()

# Delete (All)
def delete_all_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM history')
    conn.commit()
    conn.close()

# --- INIT AWAL ---
init_db()

# --- NAVIGASI SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2889/2889676.png", width=50)
    st.header("Navigasi")
    page = st.radio("Pilih Halaman:", ["🏠 Enkripsi (User)", "⚙️ Admin Database"])
    st.divider()
    st.caption(f"Server Time:\n{datetime.now().strftime('%H:%M:%S')}")

# ================= HALAMAN USER (ENKRIPSI) =================
if page == "🏠 Enkripsi (User)":
    st.title("🔒 UNO Encryption Tools")
    st.markdown("Program Enkripsi Client-Server dengan **Python Streamlit**.")

    col1, col2 = st.columns(2)
    with col1:
        key_input = st.text_input("Key Kombinasi (6 Huruf)", value="MKHBRP", max_chars=6)
    with col2:
        shift_input = st.text_input("Pola Shift (Angka)", value="12312")

    text_input = st.text_area("Plain Text", "HALO DOSEN")

    if st.button("Enkripsi Sekarang", type="primary", use_container_width=True):
        cipher = UnoCipher()
        result = cipher.encrypt(text_input, key_input, shift_input)
        
        if "Error" in result:
            st.error(result)
        else:
            st.success("Enkripsi Berhasil!")
            st.code(result, language='text')
            save_to_db(text_input, key_input, shift_input, result)
            st.toast("Data disimpan ke database.", icon="✅")

    st.divider()

# ================= HALAMAN ADMIN (CRUD) =================
elif page == "⚙️ Admin Database":
    st.title("⚙️ Dashboard Admin")

    # Sistem Login Sederhana
    if 'is_admin' not in st.session_state:
        st.session_state['is_admin'] = False

    if not st.session_state['is_admin']:
        st.warning("Area terbatas. Masukkan password admin.")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if password == "admin123":  # PASSWORD DEFAULT
                st.session_state['is_admin'] = True
                st.rerun()
            else:
                st.error("Password salah!")
    else:
        # Jika sudah login
        if st.button("Logout"):
            st.session_state['is_admin'] = False
            st.rerun()

        st.divider()
        
        # 1. READ DATA
        st.subheader("1. Data Viewer")
        df = load_history()
        st.dataframe(df, use_container_width=True)
        
        # Tombol Backup DB
        with open(DB_NAME, "rb") as f:
            st.download_button("📥 Backup/Download Database (.db)", f, file_name="backup_uno_history.db")

        st.divider()
        
        # Layout Kolom untuk Edit dan Delete
        col_edit, col_del = st.columns(2)
        
        # 2. UPDATE DATA
        with col_edit:
            st.subheader("2. Edit Data")
            id_to_edit = st.number_input("Masukkan ID untuk diedit", min_value=0, step=1)
            
            # Ambil data saat ini berdasarkan ID
            current_data = df[df['id'] == id_to_edit]
            
            if not current_data.empty:
                with st.form("edit_form"):
                    st.info(f"Mengedit ID: {id_to_edit}")
                    new_text = st.text_input("Input Text Baru", current_data.iloc[0]['input_text'])
                    new_key = st.text_input("Key Baru", current_data.iloc[0]['key_code'])
                    new_shift = st.text_input("Shift Baru", current_data.iloc[0]['shift_pattern'])
                    # Hitung ulang hasil enkripsi otomatis jika diedit
                    cipher_edit = UnoCipher()
                    new_result = cipher_edit.encrypt(new_text, new_key, new_shift)
                    st.text(f"Preview Hasil Baru: {new_result}")
                    
                    if st.form_submit_button("Update Data"):
                        update_data(id_to_edit, new_text, new_key, new_shift, new_result)
                        st.success(f"ID {id_to_edit} berhasil diupdate!")
                        st.rerun()
            else:
                st.caption("Masukkan ID yang valid dari tabel di atas.")

        # 3. DELETE DATA
        with col_del:
            st.subheader("3. Hapus Data")
            id_to_del = st.number_input("Masukkan ID untuk dihapus", min_value=0, step=1, key="del_input")
            
            if st.button("🗑️ Hapus Baris Ini", type="secondary"):
                if id_to_del in df['id'].values:
                    delete_data(id_to_del)
                    st.warning(f"Data ID {id_to_del} telah dihapus.")
                    st.rerun()
                else:
                    st.error("ID tidak ditemukan.")

            st.markdown("---")
            if st.button("⚠️ RESET SEMUA DATABASE", type="primary"):
                delete_all_data()
                st.error("Semua data telah dihapus permanen!")
                st.rerun()

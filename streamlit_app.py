import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

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
        # Validasi sederhana agar tidak error
        if not key or not shift: return "Error: Key/Shift kosong"
        
        shifts = [int(x) for x in str(shift) if x.isdigit()]
        if not shifts: return "Error: Pola Shift harus angka"
        
        grid = self._generate_grid(key)
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

# --- BAGIAN 2: DATABASE SQLITE ---
def init_db():
    conn = sqlite3.connect('uno_history.db')
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

def save_to_db(text, key, shift, result):
    conn = sqlite3.connect('uno_history.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO history (timestamp, input_text, key_code, shift_pattern, result_text) VALUES (?,?,?,?,?)',
              (timestamp, text, key, shift, result))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect('uno_history.db')
    df = pd.read_sql_query("SELECT * FROM history ORDER BY id DESC", conn)
    conn.close()
    return df

# --- BAGIAN 3: TAMPILAN STREAMLIT ---
st.set_page_config(page_title="UNO Encryption", page_icon="🔒")

# Inisialisasi Database saat pertama kali jalan
init_db()

st.title("🔒 UNO Encryption Tools")
st.markdown("Program Enkripsi Client-Server dengan **Python Streamlit** & **SQLite Database**.")

# Form Input
col1, col2 = st.columns(2)
with col1:
    key_input = st.text_input("Key Kombinasi (6 Huruf)", value="MKHBRP", max_chars=6)
with col2:
    shift_input = st.text_input("Pola Shift (Angka)", value="12312")

text_input = st.text_area("Plain Text", "HALO DOSEN")

# Tombol Proses
if st.button("Enkripsi Sekarang", type="primary"):
    cipher = UnoCipher()
    result = cipher.encrypt(text_input, key_input, shift_input)
    
    # Tampilkan Hasil
    st.success("Berhasil!")
    st.code(result, language='text')
    
    # Simpan ke Database
    save_to_db(text_input, key_input, shift_input, result)
    st.toast("Data berhasil disimpan ke Server Database!", icon="✅")

# Menampilkan History Database
st.divider()
st.subheader("📂 Riwayat Database (Server Data)")

if st.button("Refresh Data"):
    st.rerun()

df = load_history()
st.dataframe(df, use_container_width=True)

# Footer
st.caption("Dibuat oleh Ananta Ramadhani - 24.83.1062")

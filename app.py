import streamlit as st
import pandas as pd
import re
from collections import Counter

# --- FUNGSI UTAMA ANALISIS ---
def classify_digit_oe(digit):
    """Klasifikasi Ganjil (O) / Genap (E)"""
    return 'Ganjil' if int(digit) % 2 != 0 else 'Genap'

def classify_digit_bs(digit):
    """Klasifikasi Besar (B: 5-9) / Kecil (S: 0-4)"""
    return 'Besar' if int(digit) >= 5 else 'Kecil'

def analyze_patterns(raw_data):
    # Ekstrak semua angka 4 digit dari teks input menggunakan regex
    all_numbers = re.findall(r'\b\d{4}\b', raw_data)
    
    if not all_numbers:
        return None, 0

    pola_4d_oe = []
    pola_4d_bs = []
    pola_3d_oe = []
    pola_3d_bs = []
    pola_2d_oe = []
    pola_2d_bs = []

    for num in all_numbers:
        d1, d2, d3, d4 = num[0], num[1], num[2], num[3]
        
        # --- ANALISIS 4D ---
        oe_4d = [classify_digit_oe(d) for d in [d1, d2, d3, d4]]
        bs_4d = [classify_digit_bs(d) for d in [d1, d2, d3, d4]]
        
        # Format ringkasan 4D
        o_count = oe_4d.count('Ganjil')
        e_count = oe_4d.count('Genap')
        if o_count == 4: pola_4d_oe.append("Ganjil Semua")
        elif e_count == 4: pola_4d_oe.append("Genap Semua")
        else: pola_4d_oe.append(f"{o_count} Ganjil {e_count} Genap")

        b_count = bs_4d.count('Besar')
        s_count = bs_4d.count('Kecil')
        if b_count == 4: pola_4d_bs.append("Besar Semua")
        elif s_count == 4: pola_4d_bs.append("Kecil Semua")
        else: pola_4d_bs.append(f"{s_count} Kecil {b_count} Besar")

        # --- ANALISIS 3D (3 digit terakhir / d2, d3, d4) ---
        oe_3d = [classify_digit_oe(d) for d in [d2, d3, d4]]
        bs_3d = [classify_digit_bs(d) for d in [d2, d3, d4]]
        
        o_count_3d = oe_3d.count('Ganjil')
        e_count_3d = oe_3d.count('Genap')
        if o_count_3d == 3: pola_3d_oe.append("Ganjil Semua")
        elif e_count_3d == 3: pola_3d_oe.append("Genap Semua")
        else: pola_3d_oe.append(f"{o_count_3d} Ganjil {e_count_3d} Genap")

        b_count_3d = bs_3d.count('Besar')
        s_count_3d = bs_3d.count('Kecil')
        if b_count_3d == 3: pola_3d_bs.append("Besar Semua")
        elif s_count_3d == 3: pola_3d_bs.append("Kecil Semua")
        else: pola_3d_bs.append(f"{s_count_3d} Kecil {b_count_3d} Besar")

        # --- ANALISIS 2D KASUS KHUSUS (2 digit terakhir / d3, d4) ---
        oe_2d_1 = classify_digit_oe(d3)
        oe_2d_2 = classify_digit_oe(d4)
        if oe_2d_1 == 'Ganjil' and oe_2d_2 == 'Ganjil': pola_2d_oe.append("Ganjil Semua")
        elif oe_2d_1 == 'Genap' and oe_2d_2 == 'Genap': pola_2d_oe.append("Genap Semua")
        else: pola_2d_oe.append(f"{oe_2d_1} {oe_2d_2}") # Contoh: Ganjil Genap atau Genap Ganjil

        bs_2d_1 = classify_digit_bs(d3)
        bs_2d_2 = classify_digit_bs(d4)
        if bs_2d_1 == 'Besar' and bs_2d_2 == 'Besar': pola_2d_bs.append("Besar Semua")
        elif bs_2d_1 == 'Kecil' and bs_2d_2 == 'Kecil': pola_2d_bs.append("Kecil Semua")
        else: pola_2d_bs.append(f"{bs_2d_1} {bs_2d_2}") # Contoh: Kecil Besar atau Besar Kecil

    # Hitung total kemunculan
    results = {
        '4D Ganjil Genap': Counter(pola_4d_oe),
        '4D Besar Kecil': Counter(pola_4d_bs),
        '3D Ganjil Genap': Counter(pola_3d_oe),
        '3D Besar Kecil': Counter(pola_3d_bs),
        '2D Ganjil Genap': Counter(pola_2d_oe),
        '2D Besar Kecil': Counter(pola_2d_bs),
    }
    
    return results, len(all_numbers)

# --- ANTARMUKA STREAMLIT ---
st.set_page_config(page_title="Detektor Pola Angka", layout="wide", page_icon="🔢")

st.title("🔢 Detektor Pola Angka (4D, 3D, 2D)")
st.write("Masukkan data teks angka Anda di bawah ini untuk melihat pola tren dominan.")

# Area Input Data
sample_data = """29 Jun	6211					
28 Jun	7090	9004	2520	6691	2656	4669
27 Jun	4639	8302	0658	1612	9934	4544"""

raw_input = st.text_area("Paste Data Angka di Sini:", value=sample_data, height=200)

if st.button("Analisis Pola", type="primary"):
    results, total_data = analyze_patterns(raw_input)
    
    if results:
        st.success(f"Berhasil menganalisis total **{total_data}** angka 4D!")
        
        # Membuat grid layout untuk hasil visual
        col1, col2 = st.columns(2)
        
        sections = list(results.keys())
        
        # Tampilkan Hasil Analisis per Bagian
        for i, section in enumerate(sections):
            current_col = col1 if i % 2 == 0 else col2
            
            with current_col:
                st.subheader(f"📊 Pola {section}")
                
                # Urutkan dari pola terbanyak
                sorted_patterns = results[section].most_common()
                
                # Konversi ke Dataframe untuk visualisasi tabel/grafik sederhana
                df = pd.DataFrame(sorted_patterns, columns=["Nama Pola", "Jumlah"])
                df["Persentase"] = ((df["Jumlah"] / total_data) * 100).round(2).astype(str) + '%'
                
                # Desain list nomor sesuai permintaan user
                for index, row in df.iterrows():
                    st.write(f"{index+1}. **{row['Nama Pola']}** : {row['Jumlah']} kali ({row['Persentase']})")
                
                st.divider()
    else:
        st.error("Tidak ditemukan pola angka 4 digit yang valid. Pastikan format angka benar (misal: 6211, 7090).")

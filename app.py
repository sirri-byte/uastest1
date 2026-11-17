import streamlit as st
import math

# =====================================================
# KONFIGURASI
# =====================================================

st.set_page_config(page_title="Estimasi Pengisian Tangki Air Hujan", page_icon="🌧️")
st.title("🌧️ Estimasi Waktu Pengisian Tangki Air Hujan")
st.caption("Kelompok 3 - Final Project Komputasi Awan")

st.divider()

# =====================================================
# INPUT
# =====================================================

st.subheader("Data Parameter Tangki & Cuaca")

col1, col2 = st.columns(2)

with col1:
    luas_atap = st.number_input("Luas Permukaan Atap (m²)", min_value=1.0, max_value=10000.0, value=50.0, step=1.0)
    volume_tangki = st.number_input("Kapasitas Tangki Air (Liter)", min_value=10.0, max_value=100000.0, value=1000.0, step=50.0)

with col2:
    intensitas_hujan = st.number_input("Intensitas Curah Hujan (mm/jam)", min_value=0.0, max_value=500.0, value=15.0, step=1.0)
    
    jenis_atap = st.selectbox(
        "Material Atap (Koefisien Limpasan)",
        options=[
            ("Seng / Galvalum / Metal (0.90)", 0.90),
            ("Genteng Tanah Liat / Keramik (0.80)", 0.80),
            ("Dak Beton (0.75)", 0.75),
            ("Ideal / Tanpa Kehilangan Air (1.00)", 1.00)
        ],
        format_func=lambda x: x[0]
    )
    koefisien = jenis_atap[1]


# =====================================================
# PERHITUNGAN
# =====================================================

if st.button("Hitung Estimasi Waktu", type="primary"):

    # Validasi jika tidak ada hujan
    if intensitas_hujan <= 0:
        st.error("Tidak dapat menghitung waktu pengisian karena intensitas hujan 0 mm/jam (tidak hujan).")
        st.stop()

    # -------------------------------------------------
    # Menghitung debit air hujan (Liter/jam)
    # 1 mm hujan pada 1 m² = 1 Liter air
    # -------------------------------------------------
    debit_air = intensitas_hujan * luas_atap * koefisien

    # -------------------------------------------------
    # Menghitung estimasi waktu pengisian (Jam)
    # -------------------------------------------------
    waktu_jam_desimal = volume_tangki / debit_air

    # Konversi ke format Jam dan Menit
    jam = int(waktu_jam_desimal)
    menit = round((waktu_jam_desimal - jam) * 60)
    
    # Penyesuaian jika pembulatan menit mencapai 60
    if menit == 60:
        jam += 1
        menit = 0

    # =================================================
    # HASIL
    # =================================================
    
    st.success("Perhitungan selesai!")
    
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("Debit Air Tertampung", f"{debit_air:.2f} Liter/jam")
    with res_col2:
        st.metric("Estimasi Waktu Penuh", f"{jam} Jam {menit} Menit")

    # Indikator Kategori Hujan & Waktu Pengisian
    if intensitas_hujan < 5:
        st.info("Kategori Hujan Ringan: Tangki akan terisi secara perlahan.")
    elif 5 <= intensitas_hujan <= 20:
        st.info("Kategori Hujan Sedang: Pengisian tangki berjalan optimal.")
    else:
        st.warning("Kategori Hujan Lebat/Ekstrem: Tangki akan cepat penuh, pastikan saluran pembuangan (overflow) siap.")
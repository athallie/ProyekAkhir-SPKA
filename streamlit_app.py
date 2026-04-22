import streamlit as st
import pandas as pd
from views.input import render_input_page
from views.output import render_output_page

if "isInput" not in st.session_state:
    st.session_state.isInput = True

st.set_page_config(page_title="Proyek Akhir SPK", page_icon="📊", layout="wide")

if st.session_state.isInput:
    render_input_page()
else:
    render_output_page()

# // 1. Ambil input
# bobot_user = BACA_DARI_SESSION_STATE("input_bobot")
# data_mentah = BACA_FILE_DATA("alternatif_data.csv")
# konfigurasi_kriteria = BACA_KONFIGURASI("tipe_kriteria_cost_benefit")

# // 2. Eksekusi Model
# JIKA TOMBOL "Hitung Rekomendasi" DITEKAN:
#     TAMPILKAN_LOADING_SPINNER()
    
#     hasil_rekomendasi = Hitung_SAW(data_mentah, bobot_user, konfigurasi_kriteria)
    
#     // 3. Tampilkan Output
#     TAMPILKAN_TEKS("Berikut adalah rekomendasi terbaik untuk Anda:")
#     TAMPILKAN_TABEL(hasil_rekomendasi)
#     TAMPILKAN_GRAFIK_BAR(hasil_rekomendasi)

# RESULTS
## Highlight Rekomendasi; st.success/metric
###---->e.g.Rekomendasi Terbaik: Berdasarkan preferensi Anda, Alternatif X adalah pilihan paling optimal dengan skor akhir 0.895.
## Tabel Papan Peringkat (peringkat, nama alt, skor)
## Visualisasi Data (Bar chart, Radar chart)
## Transparansi Keputusan (rincian detail perhitungan; st.expander)
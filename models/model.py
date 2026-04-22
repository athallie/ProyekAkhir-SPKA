import pandas as pd
import streamlit as st

@st.cache_resource
def process(df, criterias):
    # df_results = pd.DataFrame(columns=["Rank", "Alternative", "Score"])
    df_results = pd.DataFrame({"Rank":[1,2,3], "Alternative":["Asus", "Lenovo", "Dell"], "Score": [100, 90, 80]})

    return {"results": df_results}

# FUNCTION Hitung_SAW(data_alternatif, bobot_kriteria, tipe_kriteria):
    
#     // 1. Ekstraksi Matriks Keputusan
#     matriks_X = Ambil_Nilai_Angka_Saja(data_alternatif)
    
#     // 2. Normalisasi Matriks (R)
#     matriks_R = BUAT_MATRIKS_KOSONG_SEUKURAN(matriks_X)
    
#     UNTUK SETIAP kolom_kriteria DALAM matriks_X:
#         JIKA tipe_kriteria == "Benefit":
#             nilai_maks = CARI_MAKSIMUM(kolom_kriteria)
#             matriks_R[kolom] = kolom_kriteria / nilai_maks
            
#         JIKA tipe_kriteria == "Cost":
#             nilai_min = CARI_MINIMUM(kolom_kriteria)
#             matriks_R[kolom] = nilai_min / kolom_kriteria
            
#     // 3. Perhitungan Nilai Preferensi (V)
#     skor_akhir = []
#     UNTUK SETIAP baris_alternatif DALAM matriks_R:
#         total_skor = SUM(baris_alternatif DENGAN bobot_kriteria)
#         skor_akhir.TAMBAHKAN(total_skor)
        
#     // 4. Perankingan
#     data_alternatif_dengan_skor = GABUNGKAN(data_alternatif, skor_akhir)
#     hasil_ranking = URUTKAN_MENURUN(data_alternatif_dengan_skor BERDASARKAN skor_akhir)
    
#     KEMBALIKAN hasil_ranking
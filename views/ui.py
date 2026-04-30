import streamlit as st
import pandas as pd
from utils.preprocessing import *

def change_state(state):
    st.session_state.isLanding = state

def render_card(laptops):
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for index, laptop in enumerate(laptops, start=0):
        with cols[index]:
            with st.container(border=True):
                # st.metric(laptop["name"], laptop["skor"])
                st.metric(laptop["name"], 100)# ->jgn pakai metrik
                
                col1, col2 = st.columns(2)

                with col1:
                    st.write("Prosesor")
                    st.write(laptop["nama_prosesor"])
                with col2:
                    st.write("RAM/SSD")
                    st.write(f"{laptop["ram"]}/{laptop["ssd"]}")

                col3, col4 = st.columns(2)

                with col3:
                    st.write("Harga")
                    st.write(f"Rp{laptop["harga"]}")

                with col4:
                    st.write("Berat")
                    st.write(f"{laptop["portabilitas"]}")

def render_results(profile, results):
    st.title("Top 3 Recommendations")
    st.write(f"Berdasarkan profil {profile} dengan perhitungan Simple Additive Weighting (SAW)")
    render_card(results.head(3).to_dict(orient="records"))

def render_main_screen(landing_image, product, category, criteria, isLanding):
    if isLanding == True:
        st.image(landing_image)

        st.title("Selamata Datang di Sistem Rekomendasi Laptop", text_alignment="center")
        st.markdown(
            """
            Lakukan penyesuaian pada kriteria laptop di sidebar untuk mulai mencari rekomendasi. 
            Sistem ini akan menganalisis kriteria-kriteria Anda untuk memberikan rekomendasi yang sesuai.
            """,
            text_alignment="center"
        )

        st.button("Mulai", width="stretch", type="primary", on_click=change_state, args=[False])
    else:
        # filtered_product = filter_product_by_category(product=product, category=category["Gaming"],criteria=criteria)
        # filtered_product = filter_product
        # st.write(filtered_product)
        render_results("Tes", product)

        st.button("Kembali", width="stretch", type="primary", on_click=change_state, args=[True])

def render_sidebar(categories=["No Categories Found"], available_ram=["No RAM Found"], available_ssd=["No SSD Found"], available_panel=["No Panel Found"], available_resolution=["No Resolution Found"]):
    with st.sidebar:
        st.markdown("## :material/laptop_mac: User Preferences")
        # st.divider()

        chosen_category = st.selectbox(
            "Pilih Kategori Kebutuhan",
            categories
        )

        st.markdown("### Penyesuaian Kriteria")
        # st.write("_" * 34)

        #min-max to be changed
        harga = st.slider("Harga", 0, 99999999, 1000, format="Rp%d")
        #min-max to be changed
        skor_prosesor = st.slider("Benchmark Prosesor", 0, 999999, 25, format="%d")
        ram = st.pills("RAM", available_ram, selection_mode="multi")
        ssd = st.pills("Penyimpanan (SSD)", available_ssd, selection_mode="multi")
        baterai = st.slider("Baterai", 0, 50, 1, format="%d jam")

        st.write("Panel")
        akurasi_warna = st.checkbox(*available_panel)

        st.write("Resolusi")
        resolusi = st.checkbox(*available_resolution)


        






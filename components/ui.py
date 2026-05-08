import streamlit as st
import pandas as pd
from utils.helper import *
from components.output import *
from models.model import process
import time
from utils.ai import *

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "Custom"

if "isLanding" not in st.session_state:
    st.session_state.isLanding = True

gemini_client = setup_gemini_client()

def render_results(image_url, profile, results):
    st.title("Top 3 Recommendations")
    st.caption(f"Berdasarkan profil **{profile}** dengan perhitungan Simple Additive Weighting (SAW)")
    render_card(image_url, results.head(3).to_dict(orient="records"))

    ###GEMINI
    with st.expander("✨ Gemini AI Market Insight", expanded=True):
        with st.container(height=400): 
            with st.spinner("Gemini sedang riset harga di Internet..."):
                st.write_stream(get_gemini_market_insight(gemini_client, results.head(3), st.session_state.selected_category))
            
    st.caption("Disclaimer: Output AI bersifat probabilistik dan mungkin mengandung kesalahan, halusinasi, atau informasi yang sudah usang. Harap verifikasi kembali harga dan spesifikasi secara mandiri.")

    st.markdown("---")

    st.subheader("Papan Peringkat")
    render_table_ranking(results)

def get_output_table(df, results):
    df_results = pd.DataFrame(results, columns=['index_awal', 'score'])
    df_results['rank'] = range(1, len(df_results) + 1)
    df_results['index_awal'] = df_results['index_awal'] - 1
    df_results = df_results.set_index('index_awal')

    df['score'] = df.index.map(df_results['score'])
    df['rank'] = df.index.map(df_results['rank'])

    df_sorted = df.sort_values(by='rank').reset_index(drop=True)

    return df_sorted

def render_main_screen(landing_image, product, category, criteria, criteria_mapping, unique_criteria_values):
    if st.session_state.isLanding == True:
        col1, col2, col3 = st.columns([1,3,1])
        with col2:
            st.image(landing_image)

        st.markdown("### Selamat Datang di Sistem Rekomendasi Laptop", text_alignment="center")
        st.markdown(
            f"""
            Lakukan penyesuaian pada kriteria laptop di sidebar untuk mulai mencari rekomendasi.
            Sistem ini akan menganalisis kriteria-kriteria Anda untuk memberikan rekomendasi yang sesuai.
            """,
            text_alignment="center"
        )

        st.button("Mulai", width="stretch", type="primary", on_click=change_state, args=[False])
    else:
        filters = get_filters(criteria)
        filtered_product = filter_product(product, filters)
        filtered_product_mapped = map_criteria(filtered_product, criteria_mapping)
        criteria_weights_types = get_criteria_weights_types(criteria)

        criteria_class = classify_criteria_class(
            criteria_mapping=criteria,
            criteria_values={
                "harga": st.session_state.harga,
                "prosesor": st.session_state.prosesor,
                "ram": st.session_state.ram,
                "ssd": st.session_state.ssd,
                "baterai": st.session_state.baterai,
                "portabilitas": st.session_state.portabilitas,
                "akurasi_warna": st.session_state.akurasi_warna,
                "resolusi": st.session_state.resolusi
            },
            criteria_unique_values = unique_criteria_values
        )

        # st.write(criteria_class)
        # st.write(criteria_weights_types['weights'])

        adjusted_weights = adjust_weights(
            dict(zip(criteria_weights_types["criterias"], criteria_weights_types["weights"])),
            criteria_class=criteria_class
        )

        # st.write(adjusted_weights)

        if not filtered_product_mapped.empty:
            saw_results = process(
                df=filtered_product_mapped[criteria_weights_types["criterias"]],
                weights=list(adjusted_weights.values()),
                criterion_type=criteria_weights_types["types"]
            )["results"]

            results_table = get_output_table(filtered_product, saw_results)
            render_results(landing_image, st.session_state.selected_category, results_table)
            tab1, tab2 = st.tabs(["Perbandingan", "Perhitungan"])

            with tab1:
                render_data_charts(results_table)
            with tab2:
                render_details_decision(
                    laptops=filtered_product[["name"]],
                    df=filtered_product_mapped[criteria_weights_types["criterias"]],
                    weights=list(adjusted_weights.values()),
                    criterion_type=criteria_weights_types["types"]
                )
        else:
            st.title("No laptops found, please readjust the criterias.", text_alignment="center")
            st.divider()

        st.button("Kembali", width="stretch", type="primary", on_click=change_state, args=[True])

def render_sidebar(categories=["No Categories Found"], criteria={}, criteria_values={}):
    with st.sidebar:
        st.markdown("# :material/laptop_mac: User Preferences")
        # st.divider()

        # min_values = {
        #     "harga": min(criteria_values["harga"]),
        #     "prosesor":min(criteria_values["prosesor"]),
        #     "baterai":min(criteria_values["baterai"]),
        #     "ssd":min(criteria_values["ssd"]),
        #     "ram":min(criteria_values["ram"]),
        #     "portabilitas":min(criteria_values["portabilitas"]),
        # }

        min_values = {
            "harga": 0.0,
            "prosesor":0.0,
            "baterai":0.0,
            "ssd":0,
            "ram":0,
            "portabilitas":0.0,
        }

        max_values = {
            "harga": float(max(criteria_values["harga"])),
            "prosesor":float(max(criteria_values["prosesor"])),
            "baterai":float(max(criteria_values["baterai"])),
            "ssd":max(criteria_values["ssd"]),
            "ram":max(criteria_values["ram"]),
            "portabilitas":max(criteria_values["portabilitas"]),
        }

        chosen_category = st.selectbox(
            "Pilih Kategori Kebutuhan",
            categories,
            on_change=get_criteria_preset,
            key="selected_category",
            args=[categories, criteria, max_values, criteria_values],
            index=0
        )

        disabled=(chosen_category != "Custom")

        st.markdown("### Penyesuaian Kriteria")
        harga = st.slider(
            "Harga (Rp)", 
            min_value=min_values["harga"], 
            max_value=max_values["harga"], 
            step=1000.0, 
            format="localized",
            key="harga",
            value=(min_values["harga"], max_values["harga"]),
            # disabled=disabled
        )
        skor_prosesor = st.slider(
            "Prosesor (Geekbench Score)", 
            min_value=min_values["prosesor"],
            max_value=max_values["prosesor"],
            step=1000.0, 
            format="localized",
            key="prosesor",
            value=(min_values["prosesor"], max_values["prosesor"]),
            # disabled=disabled
        )
        ram = st.pills(
            "RAM (GB)", 
            options=list(criteria_values["ram"]),
            default=list(criteria_values["ram"]),
            selection_mode="multi", 
            key="ram",
            # disabled=disabled
        )

        ssd = st.pills(
            "SSD (GB)", 
            options=list(criteria_values["ssd"]), 
            default=list(criteria_values["ssd"]),
            selection_mode="multi", 
            key="ssd",
            # disabled=disabled
        )

        baterai = st.slider(
            "Baterai", 
            min_value=min_values["baterai"], 
            max_value=max_values["baterai"], 
            step=float(1), 
            format="%d jam",
            key="baterai",
            value=(min_values["baterai"], max_values["baterai"]),
            # disabled=disabled,
        )

        portabilitas = st.slider(
            "Berat", 
            min_value=min_values["portabilitas"], 
            max_value=max_values["portabilitas"], 
            step=float(1), 
            format="%d KG",
            key="portabilitas",
            value=(min_values["portabilitas"], max_values["portabilitas"]),
            # disabled=disabled,
        )

        akurasi_warna = st.multiselect(
            label="Panel", 
            options=criteria_values["akurasi_warna"],
            default=criteria_values["akurasi_warna"],
            # disabled=disabled,
            key="akurasi_warna",
            accept_new_options=True
        )
        resolusi = st.multiselect(
            label="Resolusi", 
            options=criteria_values["resolusi"],
            default=criteria_values["resolusi"],
            # disabled=disabled,
            key="resolusi",
            accept_new_options=True
        )

def get_criteria_preset(categories, criteria, max_values, criteria_values):

    category_mapping = categories[st.session_state.selected_category]["filter"]
    criteria_filter = {}

    for key, value in category_mapping.items():
        for key1, value1 in criteria[key]["levels"].items():
            if key1 == value:
                criteria_filter[key] = value1
                
    for c, value in criteria_filter.items():
        if c not in ["akurasi_warna", "resolusi"]:
            if c in ["ram", "ssd"]:
                st.session_state[c] = [x for x in criteria_values[c] if value["min"] <= x <= value["max"]]
            else:
                st.session_state[c] = (value["min"], min(value.get("max", float('inf')), max_values[c]))
        else:
            st.session_state[c] = value
    
    criteria_unfilter = [k for k in criteria.keys() if k not in criteria_filter]

    for c in criteria_unfilter:
        if isinstance(st.session_state[c], list):
            st.session_state[c] = criteria_values[c]
        else:
            st.session_state[c] = (0, max_values[c])

def get_filters(criteria):
    filters = {}

    for c in criteria.keys():
        if isinstance(st.session_state[c], tuple):
            filters[c] = {
                "min": st.session_state[c][0],
                "max": st.session_state[c][1]
            }
        else:
            filters[c] = list(st.session_state[c])
    
    return filters

def change_state(state):
    st.session_state.isLanding = state

def render_card(image_url, laptops):
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    for index, laptop in enumerate(laptops, start=0):
        with cols[index]:
            with st.container(border=True):
                st.image(image_url)

                cola, colb = st.columns([3, 1], vertical_alignment="bottom")

                with cola:
                    st.markdown(f"<p style='font-size:1rem'><b>{laptop["name"]}<b></p>", unsafe_allow_html=True)
                # with colb:
                    # st.badge(f"{laptop["score"] * 100: .2f}")
                
                col1, col2 = st.columns(2)
                style_card_caption = 'style="color: #808495; font-size: 0.7rem; display: block; margin-bottom: -1.5rem;"'
                style_card_metrics = 'style="font-size:0.8rem; margin-top: -1rem"'

                with col1:
                    # st.caption("Prosesor")
                    # st.write(laptop["nama_prosesor"])
                    st.markdown(f"<small {style_card_caption}>Prosesor</small><br><div {style_card_metrics}>{laptop['nama_prosesor']}</div>", unsafe_allow_html=True)
                with col2:
                    ssd = laptop["ssd"] if laptop["ssd"] < 1000 else laptop["ssd"] / 1000
                    ssd_unit = "GB" if laptop["ssd"] < 1000 else "TB"

                    # st.caption("RAM / SSD")
                    # st.write(f"{laptop["ram"]} GB / {ssd} {ssd_unit}")

                    st.markdown(f"<small {style_card_caption}>RAM / SSD</small><br><div {style_card_metrics}>{laptop["ram"]} GB / {ssd} {ssd_unit}</div>", unsafe_allow_html=True)
                col3, col4 = st.columns(2)

                with col3:
                    # st.caption("Harga")
                    # st.write(f"Rp{laptop["harga"]: ,.2f}")

                    st.markdown(f"<small {style_card_caption}>Harga</small><br><div {style_card_metrics}>Rp{laptop["harga"]: ,.2f}</div>", unsafe_allow_html=True)


                with col4:
                    # st.caption("Berat")
                    # st.write(f"{laptop["portabilitas"]} KG")

                    st.markdown(f"<small {style_card_caption}>Harga</small><br><div {style_card_metrics}>{laptop["portabilitas"]} KG</div>", unsafe_allow_html=True)

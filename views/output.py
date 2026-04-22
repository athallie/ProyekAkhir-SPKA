import streamlit as st
from models import model
import pandas as pd

if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({"Rank":[1,2,3], "Alternative":["Asus", "Lenovo", "Dell"], "Score": [100, 90, 80]})

def render_highlights(results):
    recommendation = results['Alternative'].iloc[0]
    st.success(
        body=f"Rekomendasi Terbaik: {recommendation}",
        icon="🏆"
    )
    return

def render_table_ranking(results):
    st.markdown("### Papan Peringkat")
    st.dataframe(results)
    return

def render_data_charts(results):
    st.write("TEST")
    return

def render_details_decision(results):
    return

def render_output_page():
    results = model.process(
        st.session_state.df, 
        {
            "criteria1": st.session_state.criteria1, 
            "criteria2": st.session_state.criteria2, 
            "criteria3": st.session_state.criteria3
        }
    )["results"]

    render_highlights(results)
    render_table_ranking(results)
    render_data_charts(results)
    # render_details_decision()

## Highlight Rekomendasi; st.success/metric
###---->e.g.Rekomendasi Terbaik: Berdasarkan preferensi Anda, Alternatif X adalah pilihan paling optimal dengan skor akhir 0.895.
## Tabel Papan Peringkat (peringkat, nama alt, skor)
## Visualisasi Data (Bar chart, Radar chart)
## Transparansi Keputusan (rincian detail perhitungan; st.expander)
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({"Rank":[1,2,3], "Alternative":["Asus", "Lenovo", "Dell"], "Score": [100, 90, 80]})

def render_highlights(results):
    st.subheader("🏆Pemenang")

    recommendation = results['nama'].iloc[0]
    st.success(
        body=f"{recommendation}",
    )
    return

def render_table_ranking(results):
    st.subheader("Papan Peringkat")

    def highlight_top_3(row):
        default = [''] * len(row)

        gold = 'background-color: #fcf4a3; color: #5c4b00; font-weight: 700; border-bottom: 1px solid #d4af37;'
        silver = 'background-color: #f0f0f0; color: #333333; font-weight: 700; border-bottom: 1px solid #a0a0a0;'
        bronze = 'background-color: #ffd8b1; color: #5d3a1a; font-weight: 700; border-bottom: 1px solid #cd7f32;'
        default = ''

        rank_val = row['rank']

        if rank_val == 1:
            return [gold] * len(row)
        elif rank_val == 2:
            return [silver] * len(row)
        elif rank_val == 3:
            return [bronze] * len(row)
        return [default] * len(row)

    results['score'] = results['score'] * 100
    results = results[['rank', 'nama', 'score']]

    results = results.style.apply(highlight_top_3, axis=1)

    st.dataframe(
        results,
        column_config={
            'rank': st.column_config.NumberColumn(
                "Rank",
                format="%d"
            ),
            'nama': "Laptop",
            'score': st.column_config.NumberColumn(
                "Skor",
                format="%.2f"
            )
        },
        hide_index=True
    )

def create_radar_chart(df, selected_laptops, criterias):
    filtered_df = df[df['nama'].isin(selected_laptops)]
    
    fig = go.Figure()

    for index, row in filtered_df.iterrows():
        fig.add_trace(go.Scatterpolar(
            r=[row[c] for c in criterias],
            theta=criterias,
            fill='toself',
            name=row['nama']
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1]),
            angularaxis=dict(
                tickfont=dict(size=12, color="gray")
            )
        ),
        showlegend=True,
        title="Perbandingan Karakter Alternatif (Normalisasi)"
    )
    
    st.plotly_chart(fig)

def render_data_charts(results):
    st.subheader("📊 Perbandingan Skor")

    fig = px.bar(
        results, 
        x='score', 
        y='nama', 
        orientation='h',
        color='score',
        color_continuous_scale='Greens',
        text_auto='.3f'
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def render_details_decision(results):
    return

def back():
    st.session_state.isInput = True

def render_output_page():
    results = st.session_state.results['results']

    df_results = pd.DataFrame(results, columns=['index_awal', 'score'])
    df_results['rank'] = range(1, len(df_results) + 1)
    df_results['index_awal'] = df_results['index_awal'] - 1
    df_results = df_results.set_index('index_awal')

    df = st.session_state.data

    df['score'] = df.index.map(df_results['score'])
    df['rank'] = df.index.map(df_results['rank'])

    # df[['rank', 'score']] = results
    df_sorted = df.sort_values(by='rank').reset_index(drop=True)

    render_highlights(df_sorted)
    render_table_ranking(df_sorted)
    
    render_data_charts(df_sorted)

    st.button("Back", type='secondary', width="stretch", on_click=back)
    
    # criterias = list(loadFireStore('criteria').to_dict().keys())
    # selected = st.multiselect(
    #     "Pilih Laptop untuk Dibandingkan", df['nama'].tolist(),
    #     default=df['nama'].iloc[0:2].tolist()
    # )
    # create_radar_chart(df_sorted, selected, criterias)
    

## Highlight Rekomendasi; st.success/metric
###---->e.g.Rekomendasi Terbaik: Berdasarkan preferensi Anda, Alternatif X adalah pilihan paling optimal dengan skor akhir 0.895.
## Tabel Papan Peringkat (peringkat, nama alt, skor)
## Visualisasi Data (Bar chart, Radar chart)
## Transparansi Keputusan (rincian detail perhitungan; st.expander)
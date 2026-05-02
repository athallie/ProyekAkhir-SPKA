import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def render_table_ranking(results):
    results['score'] = results['score'] * 100
    results = results[['rank', 'score', 'name', 'harga', 'nama_prosesor', 'ram', 'ssd', 'baterai', 'portabilitas']]

    # results = results.style.apply(highlight_top_3, axis=1)

    results["ssd"] = results["ssd"].apply(lambda x: f"{x} GB" if x < 1000 else f"{x/1024:.1f} TB")

    st.dataframe(
        results,
        column_config={
            'name': "Laptop",
            'rank': st.column_config.NumberColumn(
                "Rank",
                format="%d"
            ),
            'nama': "Laptop",
            'score': st.column_config.NumberColumn(
                "Skor",
                format="%.2f"
            ),
            'harga': st.column_config.NumberColumn(
                "Harga",
                format="Rp%,f"
            ),
            'nama_prosesor': "Prosesor",
            'ram': st.column_config.NumberColumn(
                "RAM",
                format="%d GB"
            ),
            'ssd': "SSD",
            'baterai': st.column_config.NumberColumn(
                "Baterai",
                format="%f Jam"
            ),
            'portabilitas': st.column_config.NumberColumn(
                "Berat",
                format="%f KG"
            )
        },
        hide_index=True
    )

def render_data_charts(results):
    st.subheader("📊 Perbandingan Skor")

    fig = px.bar(
        results, 
        x='score', 
        y='name', 
        orientation='h',
        color='score',
        color_continuous_scale='Greens',
        text_auto='.3f'
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def render_details_decision(laptops, df, weights, criterion_type):
    st.subheader("🤓☝️ Transparansi Perhitungan")

    with st.expander("Persamaan Normalisasi"):
        st.markdown("##### 1. Persamaan Normalisasi")
        st.latex(r"""
        r_{ij} = \begin{cases} 
        \frac{x_{ij}}{max(x_{j})} & \text{if } j \text{ is Benefit (max)} \\
        \frac{min(x_{j})}{x_{ij}} & \text{if } j \text{ is Cost (min)} 
        \end{cases}
        """)
        
        st.markdown("##### 2. Persamaan Nilai Preferensi ($V_i$)")
        st.latex(r"V_i = \sum_{j=1}^{n} w_j \cdot r_{ij}")
    
    # 1. Normalisasi
    norm_df = df.copy().astype(float)
    
    for i, col in enumerate(df.columns):
        if criterion_type[i] == 'max':
            norm_df[col] = df[col] / df[col].max()
        else:
            norm_df[col] = df[col].min() / df[col]
            
    # 2. Pembobotan
    weighted_df = norm_df * weights
    weighted_df['skor'] = weighted_df.sum(axis=1)

    weighted_df["laptop"] = laptops
    weighted_df = weighted_df.sort_values(by='skor', ascending=True)
    
    # 3. Visualisasi
    fig = go.Figure()

    weighted_df.columns = ['Akurasi Warna', 'Baterai', 'Harga', 'Portabilitas', 'Prosesor', 'RAM', 'Resolusi', 'SSD', 'Skor', 'Laptop']
    df.columns = ['Akurasi Warna', 'Baterai', 'Harga', 'Portabilitas', 'Prosesor', 'RAM', 'Resolusi', 'SSD']

    # Tracing setiap kriteria
    for col in df.columns:
        fig.add_trace(go.Bar(
            y=weighted_df["Laptop"],
            x=weighted_df[col],
            name=col,
            orientation='h',
            hovertemplate=f"<b>{col}</b><br>Contrib: %{{x:.3f}}<br>Raw: %{{customdata}}<extra></extra>",
            customdata=df.loc[weighted_df.index, col]
        ))

    fig.update_layout(
        barmode='stack',
        title="Rincian Skor SAW (Weighted Contribution)",
        xaxis_title="Skor Akhir Preferensi (Vᵢ)",
        yaxis_title="Alternatif",
        legend_title="Kriteria",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
    )

    # Render in Streamlit
    with st.expander("Rincian Skor SAW"):
        st.plotly_chart(fig, use_container_width=True)

    # Show matrix
    with st.expander("Matriks Perhitungan"):
        st.dataframe(weighted_df.sort_values(by='Skor', ascending=False),hide_index=True)

# def render_radar_chart(df, criterias):
#     selected_laptops = st.multiselect(
#         "Pilih Laptop untuk Dibandingkan", df['name'].tolist(),
#         default=df['name'].iloc[0:2].tolist()
#     )

#     filtered_df = df[df['name'].isin(selected_laptops)]
    
#     fig = go.Figure()

#     for index, row in filtered_df.iterrows():
#         fig.add_trace(go.Scatterpolar(
#             r=[row[c] for c in criterias],
#             theta=criterias,
#             fill='toself',
#             name=row['name']
#         ))

#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(visible=True),
#             angularaxis=dict(
#                 tickfont=dict(size=12, color="gray")
#             )
#         ),
#         showlegend=True,
#         title="Perbandingan Karakter Alternatif (Normalisasi)"
#     )
    
#     st.plotly_chart(fig)

# def render_highlights(results):
#     st.subheader("🏆Pemenang")

#     recommendation = results['nama'].iloc[0]
#     st.success(
#         body=f"{recommendation}",
#     )
#     return

    # def highlight_top_3(row):
    #     default = [''] * len(row)

    #     gold = 'background-color: #fcf4a3; color: #5c4b00; font-weight: 700; border-bottom: 1px solid #d4af37;'
    #     silver = 'background-color: #f0f0f0; color: #333333; font-weight: 700; border-bottom: 1px solid #a0a0a0;'
    #     bronze = 'background-color: #ffd8b1; color: #5d3a1a; font-weight: 700; border-bottom: 1px solid #cd7f32;'
    #     default = ''

    #     rank_val = row['rank']

    #     if rank_val == 1:
    #         return [gold] * len(row)
    #     elif rank_val == 2:
    #         return [silver] * len(row)
    #     elif rank_val == 3:
    #         return [bronze] * len(row)
    #     return [default] * len(row)
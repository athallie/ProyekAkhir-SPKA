import streamlit as st
import pandas as pd
from utils.data_loader import loadFireStore
from models.model import process

if "results" not in st.session_state:
    st.session_state.results = None

if "isInput" not in st.session_state:
    st.session_state.isInput = True

def set_criteria(label):
    return st.number_input(label=label, min_value=1, max_value=100, step=1)

def normalizeWeights(df, criteria_column, value_column):
    df = df.groupby(criteria_column)[[value_column]].mean()
    df['normalized_value'] = df[value_column] / df[value_column].sum()
    return df

@st.cache_data
def load_csv_data(file):
    return pd.read_csv(file)

def set_data():
    uploaded_file = st.file_uploader("Choose a file")
    df = None
    if uploaded_file is not None:
        df = load_csv_data(uploaded_file)
        st.session_state.data = df
        st.dataframe(df.head(5))
    return df

def analyze(df, columns, weights, criterion_types):
    df_result = process(df[columns], weights, criterion_types)
    st.session_state.results = df_result
    st.session_state.isInput = False

def render_input_page():
    criteria_weights = loadFireStore("criteria").to_dict()
    criteria_mapping = loadFireStore("criteria_mapping").to_dict()
    
    criteria_mapping = {value: key for key, value in criteria_mapping.items()}
    criteria_weights = {criteria_mapping.get(k, k): v for k, v in criteria_weights.items()}
    
    sorted_criteria_weights = dict(sorted(criteria_weights.items()))
    weights = list(sorted_criteria_weights.values())

    criterion_types = ['min', 'max', 'max', 'max', 'max', 'min', 'max']

    columns = criteria_mapping.keys()

    # st.write(criteria_weights)

    st.subheader("Data Alternatif")
    df = set_data()

    if df is not None:
        st.button(label="Analyze", width="stretch", type="primary", on_click=analyze, args=[df, columns, weights, criterion_types])

    # st.subheader("Bobot Kriteria")
    # col1, col2, col3 = st.columns(3)
    # col4, col5, col6, col7 = st.columns(4)

    # with col1:
    #     harga = set_criteria("Harga")
    # with col2:
    #     prosesor = set_criteria("Prosesor")
    # with col3:
    #     ram = set_criteria("RAM")
    # with col4:
    #     penyimpanan = set_criteria("Penyimpanan")
    # with col5:
    #     baterai = set_criteria("Baterai")
    # with col6:
    #     portabilitas = set_criteria("Portabilitas")
    # with col7:
    #     kualitas_layar = set_criteria("Kualitas Layar")
    

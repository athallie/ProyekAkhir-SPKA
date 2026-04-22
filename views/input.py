import streamlit as st
import pandas as pd
from utils.data_loader import loadFireStore, test

# if st.session_state not in ["criteria1", "criteria2", "criteria3"]:
#     st.session_state.criteria1 = 0
#     st.session_state.criteria2 = 0
#     st.session_state.criteria3 = 0

firestore_docs = loadFireStore()

def set_criteria():
    criteria1 = st.slider("Criteria 1", 0, 100, 50, key="criteria1")
    criteria2 = st.slider("Criteria 2", 0, 100, 50, key="criteria2")
    criteria3 = st.slider("Criteria 3", 0, 100, 50, key="criteria3")

def set_data():
    uploaded_file = st.file_uploader("Choose a file")
    df = None
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    return df

def render_input_page():
    test(firestore_docs)
    df = set_data()
    if df is not None:
        st.dataframe(df)

    set_criteria()
    if st.button(label="Analyze"):
        st.session_state.isInput = False
        st.session_state.df = df

    

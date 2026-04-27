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
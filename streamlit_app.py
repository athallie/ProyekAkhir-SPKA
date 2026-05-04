import pandas as pd
from components.ui import *
import streamlit as st
from utils.data_loader import *
from models.model import process

if "isInput" not in st.session_state:
    st.session_state.isInput = True

if "isLanding" not in st.session_state:
    st.session_state.isLanding = True

if "sb_state" not in st.session_state:
    st.session_state.sb_state = "collapsed"

st.set_page_config(page_title="Proyek Akhir SPK", page_icon="📊", layout="wide")

###FIRESTORE
st.session_state.db = load_firestore()
st.session_state.criteria = get_documents(st.session_state.db, "criteria")
st.session_state.category = get_documents(st.session_state.db, "category")
st.session_state.criteria_mapping = get_documents(st.session_state.db, "specification_mapping")
st.session_state.product = normalize_product(get_documents(st.session_state.db, "product"))
sorted_categories = dict(sorted(st.session_state.category.items()))
sorted_categories_custom_top = {'Custom': sorted_categories.pop('Custom'), **sorted_categories}

###Unique Criteria Values
criteria_values = extract_components(st.session_state.product)

storage = load_appwrite()
landing_image = get_file_url(storage, "asset", "landing_page")

render_sidebar(
    categories=sorted_categories_custom_top,
    criteria = st.session_state.criteria,
    criteria_values=criteria_values
)
render_main_screen(
    landing_image=landing_image, 
    product=st.session_state.product, 
    category=st.session_state.category,
    criteria=st.session_state.criteria,
    criteria_mapping=st.session_state.criteria_mapping,
    unique_criteria_values=criteria_values
)
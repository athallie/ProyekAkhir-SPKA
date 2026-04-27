import pandas as pd
import numpy as np
from pyDecision.algorithm import saw_method
import streamlit as st

@st.cache_resource
def process(df, weights, criterion_type):
    my_bar = st.progress(0, text="Operation in progress...")
    array = df.to_numpy()
    
    my_bar.progress(50, text="Operation in progress...")
    #  Call Saw Function
    rank = saw_method(array, criterion_type, weights, graph = True, verbose = True)

    my_bar.progress(100, text="Operation in progress...")
    my_bar.empty()
    return {"results": rank}
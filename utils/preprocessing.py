import pandas as pd
import streamlit as st
import json

def normalize_weights(df, criteria_column, value_column):
    df = df.groupby(criteria_column)[[value_column]].mean()
    df['normalized_value'] = df[value_column] / df[value_column].sum()
    return df

def normalize_product(df):
    df = pd.json_normalize(df.values())
    df.columns = df.columns.str.replace("specification.", "", regex=False)
    # df['prosesor'] = pd.to_numeric(df['prosesor'], errors='coerce')
    # df['ram'] = pd.to_numeric(df['ram'], errors='coerce')

    return df

def filter_product_by_category(product, category, criteria):
    filter_criteria = category["filter"]
    criteria_levels = {}

    query = ""

    for index, (key, value) in enumerate(filter_criteria.items(), start=1):
        level = criteria[key]["levels"][value]
        criteria_levels[key] = level

        if isinstance(level, list):
            query += f"{key} in {level}"
        else:
            query += f"{level["min"]} < {key} < {level["max"]}"

        if index is not len(filter_criteria):
            query += " and "
        
    st.write(query)

    filtered_product = product.query(query)
   
    return filtered_product
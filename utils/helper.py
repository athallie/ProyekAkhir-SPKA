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

# def filter_product_by_category(product, category, criteria):
#     filter_criteria = category["filter"]
#     criteria_levels = {}

#     query = ""

#     for index, (key, value) in enumerate(filter_criteria.items(), start=1):
#         level = criteria[key]["levels"][value]
#         criteria_levels[key] = level

#         if isinstance(level, list):
#             query += f"{key} in {level}"
#         else:
#             query += f"{level["min"]} < {key} < {level["max"]}"

#         if index is not len(filter_criteria):
#             query += " and "
        
#     st.write(query)

#     filtered_product = product.query(query)
   
#     return filtered_product

# filters->{criteria: filters}
def filter_product(product, filters):
    query = ""

    for index, (key, value) in enumerate(filters.items(), start=1):
        if isinstance(value, list):
            query += f"{key} in {value}"
        else:
            query += f"{value["min"]} < {key} < {value["max"]}"

        if index is not len(filters):
            query += " and "
        
    # st.write(query)

    filtered_product = product.query(query)
   
    return filtered_product.reset_index(drop=True)

@st.cache_data
def extract_components(df = pd.DataFrame()):
    dict = {}

    for column in df.columns:
        dict[column] = set(df[column])
    
    return dict

# @st.cache_data
def dict_move_to_front(dict, key):
    reordered_dict = {key: dict.pop(key), **dict}
    return reordered_dict

def get_criteria_weights_types(criteria):
    criteria_weights = {}
    criteria_types = {}

    for key, value in criteria.items():
        criteria_weights[key] = value["weight"]
        criteria_types[key] = value["type"]

    sorted_criteria_weights = dict(sorted(criteria_weights.items()))
    sorted_criteria_types = dict(sorted(criteria_types.items()))

    criterias = list(sorted_criteria_weights.keys())
    weights = list(sorted_criteria_weights.values())
    types = list(sorted_criteria_types.values())

    # st.write(sorted_criteria_weights)
    # st.write(sorted_criteria_types)

    return {
        "criterias": criterias, 
        "weights": weights, 
        "types": types
    }

def map_criteria(df, criteria_mapping):
    mapped_df = df.copy()

    for key, value in criteria_mapping.items():
        mapped_df[key] =  mapped_df[key].replace(value["mapping"])

    return mapped_df

def adjust_weights(criteria_weights, selected_category, category_mapping):
    mapping = category_mapping[selected_category]["filter"]
    mapping = {k: v for k, v in mapping.items() if v != "low"}

    prioritized_criterias = {k: v for k, v in criteria_weights.items() if k in mapping.keys()}
    unprioritized_criterias = {k: v for k, v in criteria_weights.items() if k not in mapping.keys()}

    total_unprioritized_weights = 1 - sum(unprioritized_criterias.values())
    total_surplus = 0

    for k, v in prioritized_criterias.items():
        if mapping[k] == "high":
            prioritized_criterias[k] = v + 0.10
            total_surplus += 0.10
        elif mapping[k] == "mid":
            prioritized_criterias[k] = v + 0.05
            total_surplus += 0.05

    for k, v in unprioritized_criterias.items():
        unprioritized_criterias[k] = v - (total_surplus * (v/total_unprioritized_weights))

    combined_criteria_weights = prioritized_criterias | unprioritized_criterias

    total_weights_new = sum(combined_criteria_weights.values())
    for k, v in combined_criteria_weights.items():
        combined_criteria_weights[k] = v / total_weights_new

    sorted_combined_criteria_weights = dict(sorted(combined_criteria_weights.items()))
    return sorted_combined_criteria_weights
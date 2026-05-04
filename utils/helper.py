import pandas as pd
import streamlit as st
import json
from collections import Counter

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

# def adjust_weights(criteria_weights, selected_category, category_mapping):
#     mapping = category_mapping[selected_category]["filter"]

# def adjust_weights(criteria_weights, criteria_class):
#     mapping = {k: v for k, v in criteria_class.items() if v != "low"}

#     prioritized_criterias = {k: v for k, v in criteria_weights.items() if k in mapping.keys()}
#     unprioritized_criterias = {k: v for k, v in criteria_weights.items() if k not in mapping.keys()}

#     total_unprioritized_weights = 1 - sum(unprioritized_criterias.values())
#     total_surplus = 0

#     for k, v in prioritized_criterias.items():
#         if mapping[k] == "high":
#             prioritized_criterias[k] = v + 0.10
#             total_surplus += 0.10
#         elif mapping[k] == "mid":
#             prioritized_criterias[k] = v + 0.05
#             total_surplus += 0.05

#     for k, v in unprioritized_criterias.items():
#         unprioritized_criterias[k] = v - (total_surplus * (v/total_unprioritized_weights))

#     combined_criteria_weights = prioritized_criterias | unprioritized_criterias

#     total_weights_new = sum(combined_criteria_weights.values())
#     for k, v in combined_criteria_weights.items():
#         combined_criteria_weights[k] = v / total_weights_new

#     st.write(total_weights_new)

#     sorted_combined_criteria_weights = dict(sorted(combined_criteria_weights.items()))
#     return sorted_combined_criteria_weights

def adjust_weights(criteria_weights, criteria_class):
    mapping = {k: v for k, v in criteria_class.items() if v in ["high", "mid"]}
    cost_like_criterias = ["harga", "portabilitas"]
    
    new_weights = criteria_weights.copy()
    # total_surplus = 0

    for k, v in mapping.items():
        if v == "high":
            if k in cost_like_criterias:
                new_weights[k] *= 0.5 
            else:
                new_weights[k] *= 1.5 
        elif v == "mid":
            if k in cost_like_criterias:
                new_weights[k] *= 0.75
            else:
                new_weights[k] *= 1.25
        # addition = 0.10 if v == "high" else 0.05
        # new_weights[k] += addition
        # total_surplus += addition
            
        # change = 0.10 if v == "high" else 0.05
        
        # if k in cost_like_criterias:
        #     new_weights[k] -= change
        #     total_surplus -= change
        # else:
        #     new_weights[k] += change
        #     total_surplus += change

    # non_prioritized_keys = [k for k in criteria_weights.keys() if k not in mapping]
    # sum_non_prioritized = sum(criteria_weights[k] for k in non_prioritized_keys)

    # if sum_non_prioritized > 0:
    #     for k in non_prioritized_keys:
    #         adjustment = total_surplus * (criteria_weights[k] / sum_non_prioritized)
    #         new_weights[k] -= adjustment
    
    total_sum = sum(new_weights.values())
    if total_sum > 0:
            for k in new_weights:
                new_weights[k] = new_weights[k] / total_sum

    # st.write(f"Total Weight: {sum(new_weights.values())}")

    return dict(sorted(new_weights.items()))


def classify_criteria_class(criteria_mapping, criteria_values, criteria_unique_values):

    criteria_class = {}

    for crit_key, crit_val in criteria_mapping.items():
        mapping = crit_val['levels']
        
        if crit_key not in ["akurasi_warna", "resolusi", "ram", "ssd"]:
            if min(criteria_values[crit_key]) == 0 and max(criteria_values[crit_key]) == max(criteria_unique_values[crit_key]):
                criteria_class[crit_val['name']] = 'low'
                continue

            centroid = sum(criteria_values[crit_key]) / 2
            for level in mapping.keys():
                min_val = mapping[level]['min']
                max_val = mapping[level]['max']

                if min_val < centroid < max_val:
                    criteria_class[crit_val['name']] = level
        elif crit_key in ["ram", "ssd"]:
            if not criteria_values[crit_key]:
                criteria_class[crit_val['name']] = 'low'
                continue
            if Counter(criteria_values[crit_key]) == Counter([8, 16, 32, 64]) or Counter(criteria_values[crit_key]) == Counter([256, 512, 1000, 2000]):
                criteria_class[crit_val['name']] = 'low'
                continue

            max_crit = max(criteria_values[crit_key])
            for level in mapping.keys():
                min_val = mapping[level]['min']
                max_val = mapping[level]['max']

                if min_val < max_crit < max_val:
                    criteria_class[crit_val['name']] = level
        else:
            high_crit = mapping['high']
            mid_crit = mapping['mid']
            full_crit = list(criteria_unique_values[crit_key])

            crit_val_list = list(criteria_values[crit_key])

            if Counter(full_crit) == Counter(crit_val_list):
                criteria_class[crit_val['name']] = 'low'
                continue;

            if not set(high_crit).isdisjoint(crit_val_list):
                criteria_class[crit_val['name']] = 'high'
            elif not set(mid_crit).isdisjoint(crit_val_list):
                criteria_class[crit_val['name']] = 'mid'
            else:
                criteria_class[crit_val['name']] = 'low'

    # st.write(criteria_class)
    return criteria_class
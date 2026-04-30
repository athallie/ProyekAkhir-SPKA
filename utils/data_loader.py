from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from google.oauth2 import service_account
import pandas as pd
import streamlit as st
from appwrite.client import Client
from appwrite.services.storage import Storage
from appwrite.id import ID

@st.cache_resource
def load_firestore():
    creds_dict = dict(st.secrets["firestore"])
    credentials = service_account.Credentials.from_service_account_info(creds_dict)

    db = firestore.Client(credentials=credentials, project=creds_dict['project_id'])

    return db

@st.cache_resource
def get_collection(_db, name):
    return _db.collection(name)

@st.cache_resource
def get_documents(_db, collection_name, filter_query=None):
    collection = get_collection(_db, collection_name)

    docs = None

    if filter_query is not None and filter_query is not filter_query:
       docs = collection.where(filter=FieldFilter(*filter_query)).stream()
    else:
        docs = collection.stream()

    dict = {}

    if docs is not None:
        for doc in docs:
            doc_dict = doc.to_dict()
            dict[doc_dict["name"]] = doc_dict
    
    return dict

@st.cache_resource
def load_appwrite():
    client = Client()
    creds_dict = dict(st.secrets["appwrite"])

    client.set_endpoint(creds_dict["endpoint"])
    client.set_project(creds_dict["project_id"])
    client.set_key(creds_dict["api_key"])

    return Storage(client)

@st.cache_resource
def get_file_url(_storage, bucket, file_id):

    creds_dict = dict(st.secrets["appwrite"])
    bucket_id = ""

    if bucket == "asset":
        bucket_id = creds_dict["bucket_asset"]
    elif bucket == "product":
        bucket_id = creds_dict["bucket_product"]

    return _storage.get_file_preview(bucket_id=bucket_id, file_id=file_id)

@st.cache_data
def load_csv_data(file):
    return pd.read_csv(file)

# def set_data():
#     uploaded_file = st.file_uploader("Choose a file")
#     df = None
#     if uploaded_file is not None:
#         df = load_csv_data(uploaded_file)
#         st.session_state.data = df
#         st.dataframe(df.head(5))
#     return df


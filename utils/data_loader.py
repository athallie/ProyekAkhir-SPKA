from google.cloud import firestore
from google.oauth2 import service_account
import streamlit as st

@st.cache_resource
def loadFireStore():
    creds_dict = dict(st.secrets["firestore"])
    credentials = service_account.Credentials.from_service_account_info(creds_dict)

    db = firestore.Client(credentials=credentials, project=creds_dict['project_id'])

    return db.collection("proyek_spk").document("criteria").get()

def test(fields):
    st.write(fields.to_dict())
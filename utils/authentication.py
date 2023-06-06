import streamlit as st

def is_authenticated_password(password):
    return password == st.secrets['app-pass']

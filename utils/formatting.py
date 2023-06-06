import pandas as pd
import streamlit as st

def brazilian_date(df, columns):
    for column in columns:
        df[column] = pd.to_datetime(df[column]).dt.strftime('%d-%m-%Y')
    return df

def pretty_html_table(value):
    s1 = dict(selector='th', props=[('text-align', 'center')])
    s2 = dict(selector='td', props=[('text-align', 'center')])
    all_users_html_table = value.style.set_table_styles([s1, s2]).hide(axis=0).to_html()
    return st.write(f'{all_users_html_table }', unsafe_allow_html=True) 

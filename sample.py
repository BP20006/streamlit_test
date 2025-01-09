import streamlit as st
import pandas as pd

if __name__ == "__main__":

    df = pd.read_csv('data/2024-12-11.csv', sep=',')

    st.header('arxivチェック支援サイト')
    st.write(df)

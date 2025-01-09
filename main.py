import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    layout="wide",
    initial_sidebar_state="expanded"
)

top_page = st.Page(page="contents/top_page.py", title="Top", icon=":material/home:")
display_paper = st.Page(page="contents/display_paper.py", title="arXivチェック支援ツール", icon=":material/open_with:")
pg = st.navigation([top_page, display_paper])
pg.run()

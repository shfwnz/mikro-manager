import streamlit as st
import time

pages = {
    "Dashboard" : [
        st.Page("mainPage.py", title="Dashboard")
    ],  
    "Config" : [
        st.Page("page_1.py", title="page1"),
        st.Page("page_2.py", title="page2")
    ]
}

pg = st.navigation(pages)
pg.run()

with st.sidebar :

    # add_selectionBox = st.selectbox("bjir", ("sahsahjsh","sagshaghg"))

    with st.spinner("loading..."):
        time.sleep(5)
    
    st.success("Done")
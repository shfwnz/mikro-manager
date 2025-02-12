import streamlit as st
import time

pages = {
    "Config" : [
        st.Page("./pages/auth/connect.py", title="connection "),
        st.Page("./pages/change_name_router.py", title="change router name")
    ]
}

pg = st.navigation(pages)
pg.run()

with st.sidebar :

    # add_selectionBox = st.selectbox("bjir", ("sahsahjsh","sagshaghg"))

    with st.spinner("loading..."):
        time.sleep(3)
    
        if 'ssh_connection' in st.session_state:
            if st.session_state['ssh_connection']:
                st.success("SSH Connected")
            else:
                st.error("SSH Not Connected")
        else:
            st.info("SSH Connection Status: Not Attempted")
            
    
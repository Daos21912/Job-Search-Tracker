import streamlit as st
import time
import os

st.title("Job Search Copilot")

if st.button("Exit App"):
    st.warning("Shutting down... You can close this tab.")
    time.sleep(1)
    st.markdown(
        """
        <meta http-equiv="refresh" content="0; url=about:blank">
        """,
        unsafe_allow_html=True
    )
    os._exit(0)
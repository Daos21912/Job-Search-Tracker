import streamlit as st
from data_handler import load_data, load_cover_letters
import pandas as pd

st.title("Application Dashboard")

df = load_data()

if df.empty:
    st.info("No applications yet.")
else:
    cl_df = load_cover_letters()

    # Build a set of application indices that have cover letters
    cl_indices = set(cl_df["Application Index"].tolist()) if not cl_df.empty else set()

    # Build dashboard dataframe
    dashboard = df[["Company", "Role", "Date Applied", "Status", "Last Updated"]].copy()
    dashboard["Cover Letter"] = dashboard.index.map(lambda i: "✅" if i in cl_indices else "❌")

    # --- STATS ---
    st.subheader("Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Applications", len(df))
    col2.metric("With Cover Letter", len(cl_indices))
    col3.metric("Interviewing", (df["Status"] == "Interviewing").sum())
    col4.metric("Offers", (df["Status"] == "Offer").sum())

    st.divider()

    # --- FILTER ---
    show_filter = st.selectbox(
        "Show",
        options=["All", "Has Cover Letter", "Missing Cover Letter"],
        key="dash_filter"
    )

    if show_filter == "Has Cover Letter":
        filtered = dashboard[dashboard["Cover Letter"] == "✅"]
    elif show_filter == "Missing Cover Letter":
        filtered = dashboard[dashboard["Cover Letter"] == "❌"]
    else:
        filtered = dashboard

    st.dataframe(filtered, use_container_width=True)

    st.divider()

    # --- JUMP TO COVER LETTER ---
    st.subheader("Write Cover Letter for...")
    jump_index = st.number_input(
        "Row index",
        min_value=0,
        max_value=len(df)-1,
        step=1,
        key="dash_jump_index"
    )

    jump_row = df.loc[jump_index]
    st.write(f"**Selected:** {jump_row['Company']} – {jump_row['Role']}")

    if st.button("Go to Cover Letter Writer"):
        st.session_state.cl_jump_index = jump_index
        st.switch_page("pages/3_Cover_Letter.py")
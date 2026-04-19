import streamlit as st
from data_handler import load_data, delete_application

st.title("Your Applications")

df = load_data()

if df.empty:
    st.info("No applications yet.")
else:
    # --- STATS ---
    st.subheader("Complete Stats")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total", len(df))
    col2.metric("Interviewing", (df["Status"] == "Interviewing").sum())
    col3.metric("Rejected", (df["Status"] == "Rejected").sum())

    # --- FILTERING ---
    filter_col = st.selectbox(
        "Filter by",
        options=["None", "Company", "Role", "Status", "Date Applied", "Last Updated"],
        key="filter_col"
    )

    status_options = ["Applied", "Interviewing", "Rejected", "Offer"]

    if filter_col != "None":
        if filter_col == "Status":
            filter_val = st.multiselect(
                "Status",
                options=status_options,
                default=status_options,  # all selected by default = no filtering
                key="filter_val_select"
            )
            mask = df["Status"].isin(filter_val)
        elif filter_col == "Date Applied":
            col_a, col_b = st.columns(2)
            with col_a:
                date_from = st.date_input("From", value=df["Date Applied"].min().date(), key="date_from")
            with col_b:
                date_to = st.date_input("To", value=df["Date Applied"].max().date(), key="date_to")
            mask = (df["Date Applied"].dt.date >= date_from) & (df["Date Applied"].dt.date <= date_to)
        elif filter_col == "Last Updated":
            col_a, col_b = st.columns(2)
            with col_a:
                date_from = st.date_input("From", value=df["Last Updated"].dropna().min().date(), key="lu_date_from")
            with col_b:
                date_to = st.date_input("To", value=df["Last Updated"].dropna().max().date(), key="lu_date_to")
            mask = (df["Last Updated"].dt.date >= date_from) & (df["Last Updated"].dt.date <= date_to)
        else:
            filter_val = st.text_input(f"Filter value", key="filter_val_text")
            mask = df[filter_col].str.contains(filter_val, case=False, na=False)

        df_filtered = df[mask]
    else:
        df_filtered = df


    # --- DISPLAY TABLE ---
    df_display = df_filtered[["Company", "Role", "Date Applied", "Last Updated", "Status", "Link"]].reset_index().rename(columns={"index": "ID"})
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True
    )

    # --- SINGLE SELECTION ---
    st.subheader("Select Entry")

    selected_index = st.number_input(
        "Row index",
        min_value=0,
        max_value=len(df)-1,
        step=1,
        key="selected_index"
    )

    # Show context
    selected_row = df.loc[selected_index]
    st.write(f"**Selected:** {selected_row['Company']} – {selected_row['Role']}")

    # --- ACTION BUTTONS ---
    col1, col2, col3 = st.columns(3)

    # View Notes
    with col1:
        view_notes = st.button("View Notes")

    # Edit
    with col2:
        if st.button("Edit"):
            st.session_state.edit_index = selected_index
            st.switch_page("pages/1_Add_Application.py")

    # Delete
    with col3:
        if st.button("Delete"):
            delete_application(selected_index)
            st.success("Deleted!")
            st.rerun()

    if view_notes:
        notes = selected_row["Notes"]
        if notes:
            st.text_area("Notes", value=notes, height=200, disabled=True)
        else:
            st.info("No notes for this entry.")
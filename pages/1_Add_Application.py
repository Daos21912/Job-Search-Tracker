import streamlit as st
from datetime import date
from data_handler import load_data, save_data, add_application
import pandas as pd

status_options = ["Applied", "Interviewing", "Rejected", "Offer"]
editing = "edit_index" in st.session_state

# ── Redirect after save/cancel ──────────────────────────────────────────────
if st.session_state.get("redirect_to_view"):
    del st.session_state["redirect_to_view"]
    st.switch_page("pages/2_View_Applications.py")

# ── Load row data if editing ─────────────────────────────────────────────────
if editing:
    df = load_data()
    row = df.loc[st.session_state.edit_index]
    st.title("Edit Application")
else:
    row = None
    st.title("Add New Application")

# ── Cancel button (outside form so it can redirect) ─────────────────────────
if editing:
    if st.button("Cancel Editing"):
        del st.session_state.edit_index
        st.session_state.redirect_to_view = True
        st.rerun()

# ── Form ─────────────────────────────────────────────────────────────────────
with st.form("job_form", clear_on_submit=not editing):
    company = st.text_input("Company", value=row["Company"] if editing else "")
    role = st.text_input("Role", value=row["Role"] if editing else "")
    applied_date = st.date_input(
        "Date Applied",
        value=row["Date Applied"].date() if editing else date.today()
    )
    status_index = (
        status_options.index(row["Status"])
        if editing and row["Status"] in status_options
        else 0
    )
    status = st.selectbox("Status", status_options, index=status_index)
    link = st.text_input("Job Link", value=row["Link"] if editing else "")
    notes = st.text_area("Notes", value=row["Notes"] if editing else "")
    submitted = st.form_submit_button("Save Changes" if editing else "Add Application")
    last_updated = st.date_input(
        "Last Updated",
        value=date.today()  # always defaults to today, even in edit mode
    )
    if submitted:
        new_row = {
            "Company": company.strip(),
            "Role": role.strip(),
            "Date Applied": pd.Timestamp(applied_date),  # ← fix
            "Status": status,
            "Link": link,
            "Notes": notes,
            "Last Updated": pd.Timestamp(last_updated),
        }
        if editing:
            duplicate = df[
                (df["Company"].str.strip() == new_row["Company"]) &
                (df["Role"].str.strip() == new_row["Role"])
            ]
            if not duplicate.empty and st.session_state.edit_index not in duplicate.index:
                st.warning("Duplicate entry detected.")
            else:
                df.loc[st.session_state.edit_index] = new_row
                save_data(df)
                del st.session_state.edit_index
                st.session_state.redirect_to_view = True  # ← signal redirect
                st.rerun()
        else:
            success = add_application(new_row)
            if success:
                st.success("Application added!")
                st.rerun()
            else:
                st.warning("Duplicate entry detected.")
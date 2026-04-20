import streamlit as st
from data_handler import load_data, load_cover_letters, save_cover_letter, delete_cover_letter, load_cover_letter_text
import os

st.title("Cover Letter Writer")

df = load_data()

if df.empty:
    st.info("No applications yet. Add one first.")
else:
    # Pre-select from dashboard if navigated here
    default_index = st.session_state.pop("cl_jump_index", 0)

    # --- APPLICATION SELECTOR ---
    st.subheader("Select Application")
    selected_index = st.number_input(
        "Row index",
        min_value=0,
        max_value=len(df)-1,
        step=1,
        value=default_index,
        key="cl_selected_index"
    )

    selected_row = df.loc[selected_index]

    st.dataframe(
        df.loc[[selected_index], ["Company", "Role", "Date Applied", "Status"]],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --- COVER LETTER FORM ---
    st.subheader("Write Cover Letter")

    # Load existing letter into editor if chosen
    cl_df = load_cover_letters()
    prev = cl_df[cl_df["Application Index"] == selected_index] if not cl_df.empty else cl_df

    # If there are previous letters, offer to load one into the editor
    load_text = ""
    load_name = f"Cover Letter – {selected_row['Company']}"

    if not prev.empty:
        st.subheader("Previous Cover Letters")
        prev_display = prev[["Document Name", "Date Created", "File Path"]].reset_index(drop=True)
        st.dataframe(prev_display, use_container_width=True, hide_index=True)

        col_load, col_del = st.columns(2)

        with col_load:
            load_choice = st.selectbox(
                "Load into editor",
                options=["— New letter —"] + prev["Document Name"].tolist(),
                key="load_choice"
            )

        with col_del:
            del_choice = st.selectbox(
                "Delete a letter",
                options=["— Select —"] + prev["Document Name"].tolist(),
                key="del_choice"
            )
            if st.button("Delete", key="delete_cl"):
                if del_choice != "— Select —":
                    row_to_delete = prev[prev["Document Name"] == del_choice].iloc[0]
                    delete_cover_letter(row_to_delete.name, row_to_delete["File Path"])
                    st.success(f"Deleted '{del_choice}'.")
                    st.rerun()

        if load_choice != "— New letter —":
            chosen_row = prev[prev["Document Name"] == load_choice].iloc[0]
            load_text = load_cover_letter_text(chosen_row["File Path"])
            load_name = load_choice

    doc_name = st.text_input("Document Name", value=load_name)
    letter_text = st.text_area(
        "Cover Letter",
        value=load_text,
        height=400,
        placeholder="Write your cover letter here..."
    )

    if st.button("Export to DOCX"):
        if not letter_text.strip():
            st.warning("Cover letter is empty.")
        elif not doc_name.strip():
            st.warning("Please enter a document name.")
        else:
            filepath = save_cover_letter(
                selected_index,
                selected_row["Company"],
                selected_row["Role"],
                doc_name,
                letter_text
            )
            st.success(f"Saved to `{filepath}`")
            st.rerun()
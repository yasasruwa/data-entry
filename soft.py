import streamlit as st
import pandas as pd
from io import BytesIO


def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data


def main():
    st.title('Data Entry Application')

    # Session state initialization
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

    # Get column names from user
    column_input = st.text_input("Enter column names, separated by commas")
    if column_input:
        columns = column_input.split(',')
        # Create a DataFrame with specified columns if it doesn't exist
        if set(columns) != set(st.session_state.df.columns):
            st.session_state.df = pd.DataFrame(columns=columns)

        # Interface for data entry
        data = {col: st.text_input(f"Enter data for {col}") for col in columns}

        if st.button('Add to DataFrame'):
            new_data = pd.DataFrame([data])
            st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)

    # Display DataFrame
    if not st.session_state.df.empty:
        st.write(st.session_state.df)

        # Delete Functionality
        delete_index = st.selectbox("Select a record to delete (by index)", range(len(st.session_state.df)))
        if st.button('Delete Record'):
            st.session_state.df = st.session_state.df.drop(st.session_state.df.index[delete_index]).reset_index(
                drop=True)

        # Edit Functionality
        edit_index = st.selectbox("Select a record to edit (by index)", range(len(st.session_state.df)),
                                  key="edit_index")
        if 'edit_record' not in st.session_state:
            st.session_state.edit_record = {col: "" for col in st.session_state.df.columns}

        if st.button("Load Record for Editing"):
            st.session_state.edit_record = st.session_state.df.iloc[edit_index].to_dict()

        # Display the edit form if a record is loaded
        if st.session_state.edit_record:
            updated_data = {}
            for col in st.session_state.df.columns:
                updated_data[col] = st.text_input(f"Edit data for {col}", value=st.session_state.edit_record[col],
                                                  key=f"edit_{col}")
            if st.button("Update Record"):
                st.session_state.df.iloc[edit_index] = pd.Series(updated_data)
                st.session_state.edit_record = None  # Clear the edit form

        # Download button for Excel file
        if not st.session_state.df.empty:
            val = to_excel(st.session_state.df)
            st.download_button(label='Download Excel file',
                               data=val,
                               file_name='data.xlsx',
                               mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if __name__ == "__main__":
    main()

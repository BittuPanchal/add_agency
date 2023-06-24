import pandas as pd
import numpy as np
import pickle
import streamlit as st
import base64
from io import BytesIO
import os


def read_file(file):
    if file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        df = pd.read_excel(file)
    elif file.type == "application/vnd.ms-excel":
        df = pd.read_excel(file)
    elif file.type == "text/csv":
        df = pd.read_csv(file)
    else:
        raise ValueError("Unsupported file format. Only XLSX, XLS, and CSV files are supported.")
    return df


def main():
    st.title("Data Upload and Manipulation")

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Upload data
    file = st.file_uploader("Upload File", type=["xlsx", "xls", "csv"])
    if file is not None:
        df = read_file(file)

    # Add the "agency" column
    agency_values = ['Sterling, VA', 'Winchester, VA', 'Fairfield, CT', 'San Diego, CA', 'Martinsburg, WV']
    df['Agency'] = ''

    # Select agency value
    selected_agency = st.selectbox("Select an agency", agency_values)
    if st.button("Update Agency when 1st rwo is not header"):
        df['Agency'] = selected_agency
        df.at[1, 'Agency'] = "Agency"
        
    if st.button("Update Agency when 1st rwo is header"):
        df['Agency'] = selected_agency

    # Display the updated DataFrame
    st.write("Updated Data:")
    st.dataframe(df)

    # Download button
    excel_data = BytesIO()
    if file is not None:
        file_extension = os.path.splitext(file.name)[1][1:].lower()
        if file_extension == 'xlsx' or file_extension == 'xls':
            df.to_excel(excel_data, index=False, encoding='utf-8', engine='xlsxwriter')
        elif file_extension == 'csv':
            df.to_csv(excel_data, index=False, encoding='utf-8')
        else:
            st.warning("Unsupported file format. Unable to download.")
            return

        excel_data.seek(0)
        b64_excel = base64.b64encode(excel_data.read()).decode()
        href_excel = f'<a href="data:application/octet-stream;base64,{b64_excel}" download="{file.name}">Download Updated Data ({file_extension.upper()})</a>'
        st.markdown(href_excel, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
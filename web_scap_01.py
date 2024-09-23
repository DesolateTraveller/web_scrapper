import pandas as pd
import streamlit as st
from io import StringIO, BytesIO

# Function to read the .txt file content and convert it to a pandas DataFrame
def txt_to_dataframe(txt_content, delimiter):
    try:
        # Use StringIO to read the text content as a file-like object
        data = StringIO(txt_content)
        
        # Read the content into a DataFrame based on the provided delimiter
        df = pd.read_csv(data, delimiter=delimiter)
        return df
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return None

# Function to save DataFrame as Excel
def save_dataframe_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    output.seek(0)
    return output

# Streamlit app
st.title("TXT to Excel Converter")

# File uploader for .txt file
uploaded_txt_file = st.file_uploader("Upload a TXT file", type="txt")

# Delimiter input
delimiter = st.text_input("Enter the delimiter used in the TXT file (e.g., ',', '\\t', ' '):", value=",")

# Process the TXT file if it is uploaded
if uploaded_txt_file is not None:
    # Read the content of the file as a string
    txt_content = uploaded_txt_file.read().decode("utf-8")
    
    # Convert the text content to a DataFrame
    df = txt_to_dataframe(txt_content, delimiter)
    
    # Show the DataFrame and download option if conversion is successful
    if df is not None:
        st.subheader("Extracted Data")
        st.write(df)
        
        # Save DataFrame to Excel
        excel_data = save_dataframe_to_excel(df)
        
        # Provide download button
        st.download_button(
            label="Download as Excel",
            data=excel_data,
            file_name="converted_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

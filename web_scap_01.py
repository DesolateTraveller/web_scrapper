import fitz  # PyMuPDF
import pandas as pd
import streamlit as st
from io import BytesIO

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")  # Open the PDF file
    extracted_text = ""
    
    # Loop through each page and extract text
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        extracted_text += page.get_text("text")  # Extract text from the page
    
    return extracted_text

# Function to process extracted text into a structured format
def process_extracted_text(extracted_text):
    # Split lines into rows and columns (basic processing)
    rows = [line.split() for line in extracted_text.split("\n") if line.strip()]
    
    # Convert rows into a DataFrame
    df = pd.DataFrame(rows)
    return df

# Function to save DataFrame as Excel or CSV
def save_as_excel_or_csv(df, file_type):
    output = BytesIO()
    
    if file_type == "Excel":
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Extracted_Data")
        output.seek(0)
    elif file_type == "CSV":
        output.write(df.to_csv(index=False).encode('utf-8'))
        output.seek(0)
    
    return output

# Streamlit app
st.title("PDF to Excel/CSV Converter")

# File uploader for PDF
uploaded_pdf = st.file_uploader("Upload a PDF file", type="pdf")

# Select file type for download
file_type = st.selectbox("Select file type for download", ["Excel", "CSV"])

# Process PDF and allow download if a PDF is uploaded
if uploaded_pdf is not None:
    with st.spinner("Extracting text from PDF..."):
        # Extract text from the uploaded PDF
        extracted_text = extract_text_from_pdf(uploaded_pdf)
        
        # Process the extracted text into a DataFrame
        df = process_extracted_text(extracted_text)

        # Display the extracted data
        st.subheader("Extracted Data")
        st.write(df)

        # Save as Excel or CSV
        file_data = save_as_excel_or_csv(df, file_type)

        # Provide download button
        st.download_button(
            label=f"Download {file_type} file",
            data=file_data,
            file_name=f"extracted_data.{file_type.lower()}",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" if file_type == "Excel" else "text/csv"
        )

import pytesseract
from pdf2image import convert_from_path
import pandas as pd
from io import BytesIO
import streamlit as st
import tempfile
import os

# Function to convert PDF to images
def pdf_to_images(pdf_file):
    # Use a temporary file to save the uploaded PDF
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(pdf_file.read())
        temp_file_path = temp_file.name
    
    # Convert PDF to images
    images = convert_from_path(temp_file_path)
    
    # Clean up temporary file
    os.remove(temp_file_path)
    
    return images

# Function to extract text from images using Tesseract OCR
def extract_text_from_images(images):
    extracted_texts = []
    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_texts.append(text)
    return extracted_texts

# Function to structure the text data and save to Excel
def create_excel_from_text(text_data):
    data = []
    
    for text in text_data:
        # Assuming each line in the text corresponds to a row in the invoice (e.g., item details)
        lines = text.split("\n")
        for line in lines:
            columns = line.split()  # You can split by space, tab, or use regex based on your invoice structure
            if len(columns) > 1:  # Ensuring the row has more than one column
                data.append(columns)
    
    # Create DataFrame (you may need to refine the structure depending on your invoices)
    df = pd.DataFrame(data)

    # Create an Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Invoice_Data")
        writer.close()

    output.seek(0)
    return df, output

# Streamlit app to upload PDF invoices and convert to Excel
st.title("Invoice PDF to Excel Converter")

# File uploader for PDF files
uploaded_pdf = st.file_uploader("Upload PDF Invoice", type="pdf")

if uploaded_pdf is not None:
    with st.spinner("Converting PDF to images..."):
        images = pdf_to_images(uploaded_pdf)

    with st.spinner("Extracting text from images..."):
        text_data = extract_text_from_images(images)
    
    st.success("Text extracted from invoice images.")
    
    # Process the extracted text into Excel format
    df, excel_file = create_excel_from_text(text_data)
    
    # Display the DataFrame as a table in the view
    st.dataframe(df)  # Display the extracted data as a table

    # Display download button for the Excel file
    st.download_button(
        label="Download Excel file",
        data=excel_file,
        file_name="invoice_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

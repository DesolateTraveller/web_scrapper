import pytesseract
from pdf2image import convert_from_path
import pandas as pd
from io import BytesIO
import streamlit as st
import tempfile
import os
import re

# Function to convert PDF to images
def pdf_to_images(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(pdf_file.read())
        temp_file_path = temp_file.name
    
    images = convert_from_path(temp_file_path)
    
    os.remove(temp_file_path)
    
    return images

# Function to extract text from images using Tesseract OCR
def extract_text_from_images(images):
    extracted_texts = []
    for image in images:
        text = pytesseract.image_to_string(image)
        extracted_texts.append(text)
    return extracted_texts

# Function to parse text and structure data
def parse_invoice_text(text_data):
    data = []
    
    for text in text_data:
        lines = text.split("\n")
        
        for line in lines:
            # Regex patterns to extract key fields from the invoice
            invoice_number = re.search(r'Invoice Number:\s*(\S+)', line)
            invoice_date = re.search(r'Date:\s*(\S+)', line)
            item_description = re.search(r'Item Description:\s*(.*)', line)
            quantity = re.search(r'Quantity:\s*(\d+)', line)
            unit_price = re.search(r'Unit Price:\s*\$([\d.]+)', line)
            total = re.search(r'Total:\s*\$([\d.]+)', line)
            
            # If any field is found, add to the data list
            if invoice_number or invoice_date or item_description or quantity or unit_price or total:
                data.append({
                    'Invoice Number': invoice_number.group(1) if invoice_number else '',
                    'Date': invoice_date.group(1) if invoice_date else '',
                    'Item Description': item_description.group(1) if item_description else '',
                    'Quantity': quantity.group(1) if quantity else '',
                    'Unit Price': unit_price.group(1) if unit_price else '',
                    'Total': total.group(1) if total else '',
                })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    return df

# Function to create an Excel file from DataFrame
def create_excel_from_dataframe(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Invoice_Data")
        writer.close()

    output.seek(0)
    return output

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
    
    # Parse the extracted text and structure it into a DataFrame
    df = parse_invoice_text(text_data)
    
    # Create an Excel file from the DataFrame
    excel_file = create_excel_from_dataframe(df)
    
    # Display the DataFrame as a table in the view
    st.dataframe(df)  # Display the extracted data as a table

    # Display download button for the Excel file
    st.download_button(
        label="Download Excel file",
        data=excel_file,
        file_name="invoice_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

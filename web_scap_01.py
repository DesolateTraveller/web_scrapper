import streamlit as st
import os
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
import boto3

@st.cache_data(ttl="2h")
def analyze_pdf(file_path):
    pdf_reader = PdfReader(file_path)
    num_pages = len(pdf_reader.pages)
    
    # Open PDF with PyMuPDF (fitz)
    pdf_document = fitz.open(file_path)
    num_images = 0
    pdf_source = None
    
    # Analyze content
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        images = page.get_images(full=True)
        num_images += len(images)
    
    if num_images > 0:
        pdf_source = "Image"
    else:
        first_page_text = pdf_reader.pages[0].extract_text()
        if first_page_text:
            if 'excel' in first_page_text.lower():
                pdf_source = "Excel"
            elif 'document' in first_page_text.lower():
                pdf_source = "Document"
            else:
                pdf_source = "Unknown"
        else:
            pdf_source = "Unknown"
    
    return pdf_source, num_images, num_pages

def list_s3_files(bucket_name):
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    files = [item["Key"] for item in response.get("Contents", []) if item["Key"].endswith(".pdf")]
    return files

def download_s3_file(bucket_name, file_key):
    s3_client = boto3.client("s3")
    file_path = f"/tmp/{file_key.split('/')[-1]}"
    s3_client.download_file(bucket_name, file_key, file_path)
    return file_path

def main():
    st.title("PDF Analysis: Source, Image Count, and Page Count")

    option = st.selectbox("Select source", ["Upload from local", "Select from AWS S3"])

    pdf_files = []
    if option == "Upload from local":
        uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
        if uploaded_files:
            for uploaded_file in uploaded_files:
                pdf_files.append({"file_name": uploaded_file.name, "file_path": uploaded_file})
    
    elif option == "Select from AWS S3":
        bucket_name = st.text_input("Enter S3 Bucket Name")
        if bucket_name:
            s3_files = list_s3_files(bucket_name)
            selected_files = st.multiselect("Select PDF files from S3", s3_files)
            for file_key in selected_files:
                file_path = download_s3_file(bucket_name, file_key)
                pdf_files.append({"file_name": file_key.split('/')[-1], "file_path": file_path})

    if pdf_files and st.button("Analyze PDFs"):
        result_data = []
        for pdf in pdf_files:
            pdf_source, num_images, num_pages = analyze_pdf(pdf["file_path"])
            result_data.append({
                "PDF File": pdf["file_name"],
                "Source Type": pdf_source,
                "Image Count": num_images,
                "Page Count": num_pages
            })

        st.table(result_data)

if __name__ == "__main__":
    main()

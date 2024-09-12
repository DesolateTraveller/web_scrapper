import fitz  # PyMuPDF for PDF processing
import os
import streamlit as st
import tempfile

# Helper function to count the number of images in a PDF
def count_images_in_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    image_count = 0

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        image_count += len(image_list)

    pdf_document.close()
    return image_count

# Helper function to detect source type based on content analysis
def detect_pdf_source(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_content = ""
    is_excel_format = False
    is_image_based = False
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text_content += page.get_text("text")

        # Check for tables, which might indicate Excel-like structure
        tables = page.search_for("Table")  # Simple search, can be enhanced
        if tables:
            is_excel_format = True
        
        # Check for images, if most content is image-based, consider it an image PDF
        image_list = page.get_images(full=True)
        if len(image_list) > 0 and not text_content.strip():
            is_image_based = True

    pdf_document.close()

    if is_image_based:
        return "Image"
    elif is_excel_format:
        return "Excel"
    elif text_content.strip():
        return "Document"
    else:
        return "Unknown"

# Function to analyze PDFs and generate results
def analyze_pdfs(pdf_paths):
    results = []
    for pdf_path in pdf_paths:
        source_type = detect_pdf_source(pdf_path)
        image_count = count_images_in_pdf(pdf_path)
        results.append({
            "PDF File": os.path.basename(pdf_path),
            "Source Type": source_type,
            "Number of Images": image_count
        })
    return results

# Streamlit UI
st.title("PDF Source and Image Analysis")

# Provide option to either upload PDFs or select a directory
option = st.radio("Choose a method to provide PDFs:", ('Upload PDFs', 'Select a directory'))

# For uploading PDFs
pdf_files = []
if option == 'Upload PDFs':
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save uploaded files temporarily
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(uploaded_file.read())
                pdf_files.append(temp_file.name)

# For selecting a directory
elif option == 'Select a directory':
    directory = st.text_input("Enter the directory containing your PDFs:")
    if directory and os.path.exists(directory):
        pdf_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".pdf")]

# Analyze PDFs if any are provided
if pdf_files:
    with st.spinner("Analyzing PDFs..."):
        pdf_analysis_results = analyze_pdfs(pdf_files)
        if pdf_analysis_results:
            st.write("### PDF Analysis Results")
            st.table(pdf_analysis_results)
        else:
            st.write("No PDFs found or uploaded.")
else:
    st.warning("Please upload PDF files or enter a valid directory path.")

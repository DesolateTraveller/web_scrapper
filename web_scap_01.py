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
def analyze_pdfs(pdf_paths_with_names):
    results = []
    for pdf_path, pdf_name in pdf_paths_with_names:
        pdf_document = fitz.open(pdf_path)
        source_type = detect_pdf_source(pdf_path)
        image_count = count_images_in_pdf(pdf_path)
        page_count = pdf_document.page_count  # Get number of pages in the PDF
        results.append({
            "PDF File Name": pdf_name,  # Use the actual file name
            "Source Type": source_type,
            "Number of Images": image_count,
            "Number of Pages": page_count  # Include number of pages
        })
        pdf_document.close()
    return results

# Streamlit UI
st.title("PDF Source, Image, and Page Count Analysis")

# Provide option to either upload PDFs or select a path location
option = st.radio("Choose a method to provide PDFs:", ('Upload PDFs', 'Enter a path location'))

# For uploading PDFs
pdf_files_with_names = []
temp_files_to_delete = []  # Track temporary files to delete them later
if option == 'Upload PDFs':
    uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # Save uploaded files temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(uploaded_file.read())
                pdf_files_with_names.append((temp_file.name, uploaded_file.name))  # Store temp path and original file name
                temp_files_to_delete.append(temp_file.name)  # Track temp file for deletion

# For providing a path location
elif option == 'Enter a path location':
    directory = st.text_input("Enter the file path containing your PDFs:")
    if directory and os.path.exists(directory):
        # List all PDF files from the provided location path
        pdf_files_with_names = [(os.path.join(directory, file), file) for file in os.listdir(directory) if file.endswith(".pdf")]

# Analyze PDFs if any are provided
if pdf_files_with_names:
    with st.spinner("Analyzing PDFs..."):
        pdf_analysis_results = analyze_pdfs(pdf_files_with_names)
        if pdf_analysis_results:
            st.write("### PDF Analysis Results")
            st.table(pdf_analysis_results)  # Display table including PDF file names, source type, image count, and page count
        else:
            st.write("No PDFs found or uploaded.")

    # Delete the temporary files after processing
    for temp_file in temp_files_to_delete:
        if os.path.exists(temp_file):
            os.remove(temp_file)  # Delete the temp file after analysis is done
            st.write(f"Deleted temporary file: {temp_file}")
else:
    st.warning("Please upload PDF files or enter a valid path.")

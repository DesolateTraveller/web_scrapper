import fitz
import streamlit as st
from datetime import datetime

# Helper function to count images in the PDF
@st.cache_data(ttl="2h")
def count_images_in_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    image_count = 0
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        image_list = page.get_images(full=True)
        image_count += len(image_list)
    pdf_document.close()
    return image_count

# Function to detect if the PDF is image-based (contains images, P&ID symbols, or flowcharts/arrow diagrams)
@st.cache_data(ttl="2h")
def detect_pdf_source(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_content = ""
    is_pid_symbols = False
    is_flowchart = False
    is_image_based = False
    non_image_based = False
    
    # Metadata analysis (for Word, Excel, PowerPoint detection)
    metadata = pdf_document.metadata
    creator = metadata.get('creator', '').lower()
    producer = metadata.get('producer', '').lower()

    # Check metadata for non-image types
    if 'word' in creator or 'microsoft word' in producer:
        non_image_based = True
    elif 'excel' in creator or 'microsoft excel' in producer:
        non_image_based = True
    elif 'powerpoint' in creator or 'microsoft powerpoint' in producer:
        non_image_based = True

    # Iterate through the pages of the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)

        # Get text content from the page
        text_content += page.get_text("text")
        
        # Detect tables (useful for Excel PDFs)
        table_rects = page.search_for("Table")
        if table_rects or "Total" in text_content or "Amount" in text_content:
            non_image_based = True
        
        # Detect flowcharts or arrow diagrams (searching for arrow symbols)
        arrow_rects = page.search_for("→")  # Search for arrow symbols as a proxy for flowcharts
        if arrow_rects:
            is_flowchart = True

        # Detect common P&ID symbols (simple search for basic symbols used in P&ID)
        pid_symbols = page.search_for("⌀") or page.search_for("↔")  # P&ID symbols such as pipe diameters or arrows
        if pid_symbols:
            is_pid_symbols = True
        
        # Count images
        image_list = page.get_images(full=True)
        if len(image_list) > 0:
            is_image_based = True

    pdf_document.close()

    # Determine the final source type
    if is_image_based or is_flowchart or is_pid_symbols:
        return "Image"
    elif text_content.strip() or non_image_based:
        return "Non-Image"
    else:
        return "Unknown"

# Format the creation date extracted from metadata
@st.cache_data(ttl="2h")
def format_creation_date(creation_date_str):
    if creation_date_str.startswith('D:'):
        try:
            date_obj = datetime.strptime(creation_date_str[2:16], "%Y%m%d%H%M%S")
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return "Invalid Date Format"
    return "Unknown"

# Analyze multiple PDFs and return the results as a list of dictionaries
@st.cache_data(ttl="2h")
def analyze_pdfs(pdf_paths_with_names):
    results = []
    for pdf_path, pdf_name in pdf_paths_with_names:
        pdf_document = fitz.open(pdf_path)
        source_type = detect_pdf_source(pdf_path)
        image_count = count_images_in_pdf(pdf_path)
        page_count = pdf_document.page_count 

        metadata = pdf_document.metadata
        creation_date_raw = metadata.get('creationDate', 'Unknown')  # Raw creation date from metadata
        creation_date = format_creation_date(creation_date_raw)

        results.append({
            "PDF File Name": pdf_name,  
            "Source Type": source_type,
            "Number of Images": image_count,
            "Number of Pages": page_count,
            "Creation Date": creation_date
        })
        pdf_document.close()
    return results

import streamlit as st
import PyPDF2
import pandas as pd
import re
import openpyxl

# Regular expressions for extracting common invoice information
invoice_number_re = r"Invoice\sNumber:\s(\d+)"
invoice_date_re = r"Invoice\sDate:\s(\d{2}/\d{2}/\d{4})"
customer_name_re = r"Customer\sName:\s(.+)"
total_amount_re = r"Total\sAmount:\s(\d+\.\d{2})"

def extract_invoice_data(pdf_file_path):
    """Extracts invoice information from a PDF file."""
    with open(pdf_file_path, "rb") as pdf_reader:
        reader = PyPDF2.PdfReader(pdf_reader)
        text = " ".join([page.extract_text() for page in reader.pages])

        invoice_number = re.search(invoice_number_re, text).group(1)
        invoice_date = re.search(invoice_date_re, text).group(1)
        customer_name = re.search(customer_name_re, text).group(1)
        total_amount = re.search(total_amount_re, text).group(1)

        return {
            "Invoice Number": invoice_number,
            "Invoice Date": invoice_date,
            "Customer Name": customer_name,
            "Total Amount": total_amount
        }

def main():
    st.title("PDF Invoice Data Extraction")

    # Upload PDF file
    pdf_file = st.file_uploader("Upload PDF Invoice", type="pdf")

    if pdf_file:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            pdf_file.save_as(temp_file.name)
            temp_file_path = temp_file.name

        # Extract invoice data
        invoice_data = extract_invoice_data(temp_file_path)

        # Display extracted data
        st.header("Extracted Invoice Data")
        for key, value in invoice_data.items():
            st.write(f"{key}: {value}")

        # Create Excel file
        excel_file = "invoice_data.xlsx"
        df = pd.DataFrame(invoice_data, index=[0])
        df.to_excel(excel_file, index=False)

        # Download Excel file
        st.download_button(label="Download Excel", data=open(excel_file, "rb").read(), file_name=excel_file)

        # Remove the temporary file
        os.remove(temp_file_path)

if __name__ == "__main__":
    main()

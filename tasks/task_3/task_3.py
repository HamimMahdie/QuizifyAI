# Necessary imports
import streamlit as st
from PyPDF2 import PdfReader
import uuid
import tempfile
import os

class DocumentProcessor:
    def __init__(self):
        self.pages = []

    def ingest_documents(self):
        st.title("File Uploader")

        uploaded_files = st.file_uploader("Upload PDF Files", type=['pdf'], accept_multiple_files=True)

        if uploaded_files:
            for uploaded_file in uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    # Generate a unique filename
                    unique_id = uuid.uuid4().hex
                    temp_filename = f"{uploaded_file.name}_{unique_id}.pdf"
                    
                    # Save the uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
                    try:
                        # Process the PDF file
                        pdf_reader = PdfReader(tmp_file_path)
                        for page in pdf_reader.pages:
                            text = page.extract_text()
                            if text.strip():  # Only add non-empty pages
                                self.pages.append(text)
                        
                        st.success(f"Processed {uploaded_file.name}")
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")
                    finally:
                        # Clean up the temporary file
                        os.unlink(tmp_file_path)

        # Display the number of pages extracted
        if self.pages:
            st.write(f"Total pages extracted: {len(self.pages)}")
        else:
            st.warning("No documents found! Please upload PDF files.")

    def get_documents(self):
        return self.pages

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.ingest_documents()

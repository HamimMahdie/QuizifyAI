import streamlit as st
from langchain.document_loaders import PyPDFLoader

####### SCREEN 1
st.title("File Uploader")

if 'pages' not in st.session_state:
    st.session_state.pages = []

uploaded_files = st.file_uploader("Upload PDF Files", type=['pdf'], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # Process each uploaded file
        with st.spinner(f"Processing {uploaded_file.name}..."):
            # Save the uploaded file temporarily
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Load and extract pages using PyPDFLoader
            loader = PyPDFLoader(uploaded_file.name)
            extracted_pages = loader.load()
            
            # Add extracted pages to the session state
            st.session_state.pages.extend(extracted_pages)
        
        st.success(f"Processed {uploaded_file.name}")

# Display the number of pages extracted
st.write(f"Total pages extracted: {len(st.session_state.pages)}")

####### SCREEN 2
# Task 3: Document Ingestion completed
# You can add more functionality for Screen 2 here if needed
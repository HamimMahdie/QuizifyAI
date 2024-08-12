import sys
import os
import streamlit as st
sys.path.append(os.path.abspath('../../'))
from tasks.task_3.task_3 import DocumentProcessor
from tasks.task_4.task_4 import EmbeddingClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb import Client, Settings

class ChromaCollectionCreator:
    def __init__(self, document_processor, embedding_client):
        self.document_processor = document_processor
        self.embedding_client = embedding_client
        self.db = None
        self.collection = None

    def create_chroma_collection(self):
        documents = self.document_processor.get_documents()
        if not documents:
            st.warning("No documents found! Please upload PDF files first.")
            return False

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text('\n'.join(documents))

        print(f"Debug: Number of chunks created: {len(chunks)}")
        print(f"Debug: First chunk: {chunks[0][:100]}...")

        # Create the Chroma Collection
        try:
            # Initialize Chroma client
            self.db = Client(Settings(persist_directory="./chroma_db"))

            # Create a collection
            self.collection = self.db.create_collection(
                name="my_collection",
                embedding_function=self.embedding_client  # Ensure this is the correct method
            )

            # Process chunks in batches
            batch_size = 20  # Adjust this based on your embedding model's capabilities
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i+batch_size]
                ids = [str(j) for j in range(i, min(i+batch_size, len(chunks)))]

                # Add documents to the collection
                self.collection.add(
                    documents=batch,
                    ids=ids
                )

            st.success("Successfully created Chroma Collection!", icon="✅")
            print(f"Debug: Successfully created Chroma Collection with {len(chunks)} documents")
            return True
        except Exception as e:
            st.error(f"Failed to create Chroma Collection: {str(e)}", icon="🚨")
            print(f"Debug: Failed to create Chroma Collection: {str(e)}")
            print(f"Debug: Embed model type: {type(self.embedding_client)}")
            print(f"Debug: Embed model attributes: {dir(self.embedding_client)}")
            return False

    def retrieve_documents(self, query):
        if not self.collection:
            raise ValueError("Chroma collection is not created")
        # Implement retrieval logic here
        results = self.collection.query(query_texts=[query])
        return results

    def get_retriever(self):
        if not self.collection:
            raise ValueError("Chroma collection is not created")
        return self.collection  # Assuming this returns a compatible retriever

if __name__ == "__main__":
    processor = DocumentProcessor()
    processor.ingest_documents()
    
    print(f"Debug: Ingested documents: {processor.get_documents()}")

    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "quizzify-428916",
        "location": "us-central1"
    }
    
    embed_client = EmbeddingClient(**embed_config)
    
    chroma_creator = ChromaCollectionCreator(processor, embed_client)
    
    with st.form("Load Data to Chroma"):
        st.write("Select PDFs for Ingestion, then click Submit")
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            success = chroma_creator.create_chroma_collection()
            
            if success:
                st.write("Chroma Collection created successfully!")
            else:
                st.error("Failed to create Chroma Collection. Please try again.")

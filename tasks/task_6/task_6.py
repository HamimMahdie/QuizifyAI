import sys
import os
import streamlit as st
sys.path.append(os.path.abspath('../../'))
from tasks.task_3.task_3 import DocumentProcessor
from tasks.task_4.task_4 import EmbeddingClient
from tasks.task_5.task_5 import ChromaCollectionCreator

if __name__ == "__main__":
    st.header("Quizzify")

    # Configuration for EmbeddingClient
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "quizzify-428916",
        "location": "us-central1"
    }
    
    screen = st.empty() # Screen 1, ingest documents
    with screen.container():
        st.header("Quizzify")
        
        # 1) Initialize DocumentProcessor and Ingest Documents from Task 3
        processor = DocumentProcessor()
        processor.ingest_documents()

        # 2) Initialize the EmbeddingClient from Task 4 with embed config
        embed_client = EmbeddingClient(**embed_config)

        # 3) Initialize the ChromaCollectionCreator from Task 5
        chroma_creator = ChromaCollectionCreator(processor, embed_client)

        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            # 4) Use streamlit widgets to capture the user's input for the quiz topic and the desired number of questions
            topic_input = st.text_input("Enter the quiz topic:")
            num_questions = st.slider("Number of questions:", min_value=1, max_value=10, value=5)
            
            document = None
            
            submitted = st.form_submit_button("Generate a Quiz!")
            if submitted:
                # 5) Use the create_chroma_collection() method to create a Chroma collection from the processed documents
                chroma_creator.create_chroma_collection()
                
                # Query the Chroma collection
                document = chroma_creator.query_chroma_collection(topic_input)
                
    if document:
        screen.empty() # Screen 2
        with st.container():
            st.header("Query Chroma for Topic, top Document: ")
            st.write(document)

    # Add a section to display the generated quiz
    if document:
        st.header("Generated Quiz")
        st.write(f"Topic: {topic_input}")
        st.write(f"Number of questions: {num_questions}")
        
        # Here you would typically use an LLM to generate questions based on the document
        # For this example, we'll just display placeholder questions
        for i in range(num_questions):
            st.subheader(f"Question {i+1}")
            st.write(f"This is a placeholder question about {topic_input} based on the retrieved document.")
            st.text_input(f"Your answer for question {i+1}:")

        st.button("Submit Quiz")
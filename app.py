import streamlit as st
import os
import sys
sys.path.append(os.path.abspath('../../'))
from Document_Processor import DocumentProcessor
from Embedding_Client import EmbeddingClient
from Chroma_Collection_Creator import ChromaCollectionCreator
from Generate_Question import QuizGenerator
from Quiz_Manager import QuizManager

if __name__ == "__main__":
    
    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "quizzify-428916",
        "location": "us-central1"
    }
    
    # Add Session State
    if 'question_bank' not in st.session_state or len(st.session_state['question_bank']) == 0:

        st.session_state["question_bank"]=[]
        screen = st.empty()
        with screen.container():
            st.header("Quiz Builder")
            
            # Create a new st.form flow control for Data Ingestion
            with st.form("Load Data to Chroma"):
                st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
                
                processor = DocumentProcessor()
                processor.ingest_documents()
            
                embed_client = EmbeddingClient(**embed_config) 
            
                chroma_creator = ChromaCollectionCreator(processor, embed_client)
                topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
                questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
               
                submitted = st.form_submit_button("Submit")
                
                if submitted:
                    chroma_creator.create_chroma_collection()
                        
                    if len(processor.pages) > 0:
                        st.write(f"Generating {questions} questions for topic: {topic_input}")
                    
                    generator = QuizGenerator(topic_input, questions, chroma_creator)
                    # Initialize a QuizGenerator class using the topic, number of questrions, and the chroma collection
        
                    question_bank = generator.generate_quiz()
                    # Initialize the question bank list in st.session_state
                    st.session_state["question_bank"]= question_bank
                   
                    # Set a display_quiz flag in st.session_state to True
                    st.session_state["display_quiz"]= True
                    # Set the question_index to 0 in st.session_state
                    st.session_state["question_index"]= 0
                    st.rerun() 
    elif st.session_state["display_quiz"]:
        
        st.empty()
        with st.container():
            st.header("Generated Quiz Question: ")
            quiz_manager = QuizManager(st.session_state['question_bank'])

            # Format the question and display it
            with st.form("MCQ"):
                # Set index_question using the Quiz Manager method get_question_at_index passing the st.session_state["question_index"]
                index_question = quiz_manager.get_question_at_index(st.session_state["question_index"])
                # Unpack choices for radio button
                choices = []
                for choice in index_question['choices']:
                    key = choice['key']
                    value = choice['value']
                    choices.append(f"{key}) {value}")
                
                # Display the Question
                st.write(f"{st.session_state['question_index'] + 1}. {index_question['question']}")
                answer = st.radio(
                    "Choose an answer",
                    choices,
                    index = None
                )
                
                answer_choice = st.form_submit_button("Submit")
            
                st.form_submit_button("Next Question", on_click=lambda: quiz_manager.next_question_index(direction=1))
                st.form_submit_button("Previous Question", on_click=lambda: quiz_manager.next_question_index(direction=-1))
                if answer_choice and answer is not None:
                    correct_answer_key = index_question['answer']
                    if answer.startswith(correct_answer_key):
                        st.success("Correct!")
                    else:
                        st.error("Incorrect!")
                    st.write(f"Explanation: {index_question['explanation']}")
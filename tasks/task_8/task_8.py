import streamlit as st
import os
import sys
import json
sys.path.append(os.path.abspath('../../'))


from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
import streamlit as st
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate
import os
import sys
sys.path.append(os.path.abspath('../../'))


import streamlit as st
from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate
import os
import sys
sys.path.append(os.path.abspath('../../'))


import json

class QuizGenerator:
    def __init__(self, topic=None, num_questions=1, vectorstore=None):
        self.topic = topic or "General Knowledge"
        self.num_questions = min(num_questions, 10)
        self.vectorstore = vectorstore
        self.llm = None
        self.system_template = """
            You are a subject matter expert on the topic: {topic}
            
            Follow the instructions to create a quiz question:
            1. Generate a question based on the topic provided and context as key "question"
            2. Provide 4 multiple choice answers to the question as a list of key-value pairs "choices"
            3. Provide the correct answer for the question from the list of answers as key "answer"
            4. Provide an explanation as to why the answer is correct as key "explanation"
            
            You must respond as a JSON object with the following structure:
            {{
                "question": "<question>",
                "choices": [
                    {{"key": "A", "value": "<choice>"}},
                    {{"key": "B", "value": "<choice>"}},
                    {{"key": "C", "value": "<choice>"}},
                    {{"key": "D", "value": "<choice>"}}
                ],
                "answer": "<answer key from choices list>",
                "explanation": "<explanation as to why the answer is correct>"
            }}
            
            Context: {context}
            """
    
    def init_llm(self):
        arguments = {
            "temperature": 0.3,
            "max_output_tokens": 1000
        }
        self.llm = VertexAI(model_name='gemini-pro', **arguments)
        
    def generate_quiz(self):
        self.init_llm()
        if not self.vectorstore:
            raise ValueError("vectorstore not provided")
        
        from langchain_core.runnables import RunnablePassthrough, RunnableParallel

        retriever = self.vectorstore.get_retriever()  # Ensure the retriever is correctly initialized
        prompt_template = PromptTemplate.from_template(self.system_template)
        
        setup_and_retrieval = RunnableParallel(
            {"context": retriever, "topic": RunnablePassthrough()}
        )
        
        chain = setup_and_retrieval | prompt_template | self.llm
        
        responses = []
        for _ in range(self.num_questions):
            response = chain.invoke(self.topic)
            responses.append(json.loads(response))
        return responses




# Test the Object
if __name__ == "__main__":

    from tasks.task_3.task_3 import DocumentProcessor
    from tasks.task_4.task_4 import EmbeddingClient
    from tasks.task_5.task_5 import ChromaCollectionCreator

    embed_config = {
        "model_name": "textembedding-gecko@003",
        "project": "quizzify-428916",
        "location": "us-central1"
    }
    
    screen = st.empty()
    with screen.container():
        st.header("Quiz Builder")
        processor = DocumentProcessor()
        processor.ingest_documents()
    
        embed_client = EmbeddingClient(**embed_config)  # Initialize from Task 4
    
        chroma_creator = ChromaCollectionCreator(processor, embed_client)

        question = None
    
        with st.form("Load Data to Chroma"):
            st.subheader("Quiz Builder")
            st.write("Select PDFs for Ingestion, the topic for the quiz, and click Generate!")
            
            topic_input = st.text_input("Topic for Generative Quiz", placeholder="Enter the topic of the document")
            questions = st.slider("Number of Questions", min_value=1, max_value=10, value=1)
            
            submitted = st.form_submit_button("Submit")
            if submitted:
                chroma_creator.create_chroma_collection()
                
                st.write(topic_input)
                
                # Test the Quiz Generator
                generator = QuizGenerator(topic_input, questions, chroma_creator)
                question = generator.generate_question_with_vectorstore()

    if question:
        screen.empty()
        with st.container():
            st.header("Generated Quiz Question: ")
            st.write(question)